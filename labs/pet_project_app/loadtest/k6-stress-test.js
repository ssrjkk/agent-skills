import http from 'k6/http';
import { check, sleep } from 'k6';

// Нагрузочное тестирование микросервиса с автоматической проверкой SLO
// Запуск: k6 run loadtest/k6-stress-test.js
export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Плавный разогрев до 20 виртуальных пользователей
    { duration: '1m',  target: 100 }, // Пиковая нагрузка 100 параллельных клиентов
    { duration: '20s', target: 0 },   // Плавное остывание (Scale down)
  ],
  thresholds: {
    // Наш SLO: 95% запросов должны быть быстрее 150ms, а 99% — быстрее 250ms
    http_req_duration: ['p(95)<150', 'p(99)<250'],
    // Процент ошибок должен быть строго меньше 0.5%
    http_req_failed: ['rate<0.005'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export default function () {
  const res = http.get(`${BASE_URL}/api/orders`);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'has trace_id header': (r) => r.headers['X-Trace-Id'] !== undefined,
  });

  sleep(0.1);
}
