// CLI-утилита для генерации команд очистки Evicted и Failed подов в Kubernetes
package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
)

func main() {
	namespace := os.Getenv("NAMESPACE")
	args := []string{"get", "pods", "--field-selector=status.phase==Failed", "-o", "jsonpath={range .items[*]}{.metadata.namespace}{" "}{.metadata.name}{"\n"}{end}"}
	if namespace != "" {
		args = append(args, "-n", namespace)
	} else {
		args = append(args, "-A")
	}

	out, err := exec.Command("kubectl", args...).CombinedOutput()
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to list failed pods: %v (%s)
", err, string(out))
		os.Exit(1)
	}

	lines := strings.Split(strings.TrimSpace(string(out)), "
")
	cleaned := 0
	for _, line := range lines {
		if line == "" {
			continue
		}
		parts := strings.Fields(line)
		if len(parts) == 2 {
			ns, pod := parts[0], parts[1]
			fmt.Printf("[CLEANUP] Deleting failed pod %s/%s
", ns, pod)
			_ = exec.Command("kubectl", "delete", "pod", pod, "-n", ns, "--wait=false").Run()
			cleaned++
		}
	}
	fmt.Printf("Done. Total pods scheduled for deletion: %d
", cleaned)
}
