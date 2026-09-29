---
name: expo-rn
description: "Expo SDK for React Native development"
category: mobile
tags: [expo, react-native, mobile, ios, android, cross-platform]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# Expo SDK

> Build cross-platform mobile apps with Expo SDK and React Native.

## Quick Start
```tsx
// app/index.tsx — Expo Router file-based routing
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
# Create and develop
npx create-expo-app my-app --template blank-typescript
cd my-app
npx expo start

# Native builds
npx expo run:ios    # iOS simulator
npx expo run:android  # Android emulator

# Production builds
eas build --platform all
eas submit --platform ios
eas submit --platform android

# OTA updates
npx expo update
```

## Key Concepts
Expo provides a managed workflow with built-in APIs (camera, location, SQLite, notifications, auth). Expo Router provides file-based navigation. EAS Build handles native compilation. OTA updates skip app store review.

## When to Use
- Cross-platform iOS + Android apps from one codebase
- Apps needing native features (camera, GPS, biometrics)
- MVPs requiring fast iteration with OTA updates
- Teams wanting to avoid native build tooling setup

## Step-by-Step
1. Scaffold: `npx create-expo-app my-app --template blank-typescript`, then `cd my-app && npx expo start`.
2. Add routing: install `expo-router` and use file-based routes under `app/` (or run with the default router template).
3. Configure native APIs: run `npx expo install expo-camera expo-location expo-sqlite` and add the plugin config in `app.json`.
4. Develop on device: open in Expo Go or run `npx expo run:ios`/`run:android` for a native dev build.
5. Store data locally: use `expo-sqlite` (SQL via `db.getAllAsync`) or AsyncStorage for key-value state.
6. Ship: `eas build --platform all`, then `eas submit`; iterate with `npx expo update` (OTA).

## Examples
```tsx
// app/todo/[id].tsx — dynamic route with local SQLite
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
# Native build & OTA
npx expo prebuild
eas build --platform android --profile preview
npx expo update
```

## Validation
1. `npx expo start` launches Metro bundler successfully
2. App renders on both iOS simulator and Android emulator
3. Native features (camera, SQLite) work on both platforms
4. `eas build` produces installable binaries
