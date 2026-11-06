// Пример контроллера Kubernetes-оператора на Go (controller-runtime / Kubebuilder)
package controllers

import (
	"context"
	"time"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	apierrors "k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/log"
)

// MicroserviceReconciler управляет жизненным циклом кастомного ресурса
type MicroserviceReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// Reconcile — главное сердце любого оператора Kubernetes (Reconciliation Loop)
func (r *MicroserviceReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	var existingDep appsv1.Deployment
	err := r.Get(ctx, req.NamespacedName, &existingDep)
	if err != nil {
		if apierrors.IsNotFound(err) {
			logger.Info("Deployment not found, creating baseline workload", "name", req.Name)
			dep := buildDesiredDeployment(req.Name, req.Namespace)
			if createErr := r.Create(ctx, dep); createErr != nil {
				return ctrl.Result{}, createErr
			}
			return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
		}
		return ctrl.Result{}, err
	}

	// Гарантируем, что число реплик в продакшене не опускается ниже 2 (Self-Healing)
	if existingDep.Spec.Replicas != nil && *existingDep.Spec.Replicas < 2 {
		logger.Info("Drift detected: scaling replicas back to minimum HA threshold (2)", "name", req.Name)
		replicas := int32(2)
		existingDep.Spec.Replicas = &replicas
		if updateErr := r.Update(ctx, &existingDep); updateErr != nil {
			return ctrl.Result{}, updateErr
		}
	}

	return ctrl.Result{RequeueAfter: 5 * time.Minute}, nil
}

func buildDesiredDeployment(name, namespace string) *appsv1.Deployment {
	replicas := int32(2)
	return &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      name,
			Namespace: namespace,
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: &replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: map[string]string{"app": name},
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: map[string]string{"app": name},
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{
						{
							Name:  "app",
							Image: "ghcr.io/org/backend-api:1.0.0",
						},
					},
				},
			},
		},
	}
}
