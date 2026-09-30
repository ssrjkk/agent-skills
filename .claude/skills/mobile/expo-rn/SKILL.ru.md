---
name: expo-rn
description: "Expo SDK for React Native development"
category: mobile
tags: [expo-rn, mobile, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: expo-rn
---
# Expo SDK

> Создавайте кросс-платформенные мобильные приложения с Expo SDK и React Native.

## Быстрый старт
```tsx
// app/index.tsx — file-based роутинг Expo Router
import { router } from 'expo-router';
import { View, Text, FlatList, TouchableOpacity } from 'react-native';
import { useSQLiteContext } from 'expo-sqlite';

export default function HomeScreen() {
  const db = useSQLiteContext();

  const [items, setItems] = useState<Todo[]>([]);

  useEffect(() => {
    db.getAllAsync('SELECT * FROM todos ORDER BY created_at DESC')
      .then(setItems);
  }, []);

  return (
    <View className="flex-1 p-4">
      <FlatList
        data={items}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity
            onPress={() => router.push(`/todo/${item.id}`)}
            className="p-3 bg-white rounded-lg mb-2 shadow"
          >
            <Text className={`text-lg ${item.completed ? 'line-through text-gray-400' : ''}`}>
              {item.title}
            </Text>
          </TouchableOpacity>
        )}
      />
      <TouchableOpacity
        onPress={() => router.push('/todo/new')}
        className="bg-blue-500 p-4 rounded-full absolute bottom-8 right-8 shadow-lg"
      >
        <Text className="text-white text-2xl text-center">+</Text>
      </TouchableOpacity>
    </View>
  );
}
```

```bash
# Создание и разработка
npx create-expo-app my-app --template blank-typescript
cd my-app
npx expo start

# Нативные сборки
npx expo run:ios    # iOS-симулятор
npx expo run:android  # Android-эмулятор

# Продакшн-сборки
eas build --platform all
eas submit --platform ios
eas submit --platform android

# OTA-обновления
npx expo update
```

## Ключевые концепции
Expo даёт managed workflow со встроенными API (камера, геолокация, SQLite, уведомления, auth). Expo Router — file-based навигация. EAS Build делает нативную компиляцию. OTA-обновления минуют ревью в сторах.

## Когда использовать
- Кросс-платформенные iOS + Android из одной кодовой базы
- Приложения с нативными фичами (камера, GPS, биометрия)
- MVP с быстрой итерацией и OTA-обновлениями
- Команды без настройки нативной сборки

## Пошаговое руководство
1. Скаффолд: `npx create-expo-app my-app --template blank-typescript`, затем `cd my-app && npx expo start`.
2. Роутинг: установите `expo-router` и используйте file-based маршруты в `app/`.
3. Нативные API: `npx expo install expo-camera expo-location expo-sqlite` и плагин-конфиг в `app.json`.
4. Разработка на устройстве: откройте в Expo Go или `npx expo run:ios`/`run:android` для нативного dev-билда.
5. Локальные данные: `expo-sqlite` (SQL через `db.getAllAsync`) или AsyncStorage для key-value состояния.
6. Релиз: `eas build --platform all`, затем `eas submit`; итерации через `npx expo update` (OTA).

## Примеры
```tsx
// app/todo/[id].tsx — динамический маршрут с локальным SQLite
import { useLocalSearchParams } from 'expo-router';
import { useSQLiteContext } from 'expo-sqlite';
import { View, Text } from 'react-native';

export default function TodoDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const db = useSQLiteContext();
  const todo = db.getFirstSync('SELECT * FROM todos WHERE id = ?', [id]);

  return (
    <View className="p-4">
      <Text className="text-xl">{todo?.title}</Text>
      <Text>{todo?.completed ? 'Done' : 'Pending'}</Text>
    </View>
  );
}
```
```bash
# Нативная сборка и OTA
npx expo prebuild
eas build --platform android --profile preview
npx expo update
```

## Лучшие практики
- Expo SDK с Expo Go для быстрой итерации.
- Зависимости через `expo install` для совместимых версий.
- Типизированные компоненты и хуки для общей логики.
- Deep links и навигация через expo-router.
- Оптимизация изображений; expo-av аккуратно.
- Тестируйте на обеих платформах; сборки через EAS.

## Устранение неполадок
- Несовпадение версий: `npx expo install --fix`.
- Фейлы сборки: проверьте EAS-креды и app config.
- Нет нативного модуля: prebuild и config plugin.
- Медленный reload: разбейте бандл и уберите тяжёлые импорты.

## Валидация
1. `npx expo start` запускает Metro Bundler успешно
2. Приложение рендерится на iOS-симуляторе и Android-эмуляторе
3. Нативные фичи (камера, SQLite) работают на обеих платформах
4. `eas build` собирает устанавливаемые бинарники
