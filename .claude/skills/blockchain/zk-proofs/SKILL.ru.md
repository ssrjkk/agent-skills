---
name: zk-proofs
description: "Zero-knowledge proof development"
category: blockchain
tags: [zk-proofs, blockchain, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: zk-proofs
---
# Zero-Knowledge Proofs (ZK-Proofs)

> Создавайте zero-knowledge-схемы на Circom и интегрируйте их в dApp.

## Быстрый старт
```circom
// age-check.circom — доказать возраст >= 18, не раскрывая сам возраст
pragma circom 2.1.0;

include "circomlib/comparators.circom";

template AgeCheck(maxAgeBits) {
    signal input age;
    signal input threshold;
    signal output isAdult;

    component gt = GreaterEqThan(maxAgeBits);
    gt.in[0] <== age;
    gt.in[1] <== threshold;
    isAdult <== gt.out;
}

component main { public [threshold] } = AgeCheck(8);
```

```javascript
// Генерация доказательства через snarkjs
import { buildPoseidon } from "circomlibjs";

async function generateProof() {
    // Компиляция схемы
    // circom age-check.circom --r1cs --wasm --sym

    // Генерация ключей proving/verification
    // snarkjs groth16 setup age-check.r1cs pot12_final.ptau circuit.zkey

    // Генерация witness и доказательства
    const { proof, publicSignals } = await snarkjs.groth16.fullProve(
        { age: 25, threshold: 18 },
        "age-check.wasm",
        "circuit_final.zkey"
    );

    // Верификация доказательства
    const vKey = JSON.parse(fs.readFileSync("verification_key.json"));
    const verified = await snarkjs.groth16.verify(
        vKey,
        publicSignals,
        proof
    );

    console.log("Proven age >= 18:", verified);
    return { proof, publicSignals };
}
```

## Ключевые концепции
ZK-доказательства позволяют доказать утверждение, не раскрывая входные данные. Circom описывает арифметические схемы. Groth16 даёт маленькие быстро проверяемые доказательства. Типичные применения: приватные транзакции, проверка личности и масштабирование (zk-rollups).

## Когда использовать
- Приложения с защитой приватности (приватное голосование, личность)
- Масштабирование блокчейна (zk-rollups, validiums)
- Верифицируемые вычисления (аутсорс вычислений с доказательством)
- Комплаенс (доказать возраст, KYC, кредитный рейтинг без раскрытия данных)

## Пошаговое руководство
1. Напишите схему на Circom: `circom age-check.circom --r1cs --wasm --sym` компилирует в ограничения, wasm и символы.
2. Сгенерируйте powers-of-tau: `snarkjs powersoftau new bn128 12 pot12_0000.ptau`, затем `snarkjs powersoftau prepare phase2`.
3. Постройте ключи proving + verification: `snarkjs groth16 setup circuit.r1cs pot12_final.ptau circuit.zkey`.
4. Экспортируйте verification key и Solidity-верификатор: `snarkjs zkey export verificationkey` и `snarkjs zkey export solidityverifier`.
5. Вычислите witness офлайн через `snarkjs wtns calculate`, затем сгенерируйте доказательство через `groth16 prove`.
6. Верифицируйте в dApp: вызовите on-chain верификатор (или `snarkjs groth16 verify`) с public inputs и proof.

## Примеры
```javascript
// Клиентская генерация доказательства для приватной проверки возраста
import { buildPoseidon } from "circomlibjs";
import snarkjs from "snarkjs";
import fs from "fs";

const wc = await snarkjs.wtns.calculate(
  { age: 25, threshold: 18 },
  "age-check.wasm",
  "witness.wtns"
);
const { proof, publicSignals } = await snarkjs.groth16.prove(
  "circuit_final.zkey",
  "witness.wtns"
);

const vkey = JSON.parse(fs.readFileSync("verification_key.json", "utf8"));
const ok = await snarkjs.groth16.verify(vkey, publicSignals, proof);
console.log("age >= 18 proven:", ok, "public threshold:", publicSignals[0]);
```
```bash
# On-chain: разверните Verifier.sol и верифицируйте по packed call data
snarkjs zkey export solidityverifier circuit_final.zkey Verifier.sol
snarkjs generatecall
# вставьте возвращённые входные данные в `verifier.verifyProof(...)`
```

## Лучшие практики
- Логика схемы минимальна и аудируема; используйте проверенные шаблоны.
- Circom для арифметических схем; тесты через witness generation.
- Доказательства через snarkjs; закрепите trusted setup.
- Валидируйте публичные входы on-chain до верификации.
- Артефакты trusted setup версионируйте и подписывайте.
- Профилируйте число ограничений; упрощайте под лимиты.

## Устранение неполадок
- Переполнение ограничений: рефакторинг или разбиение схемы.
- Несовпадение доказательства: тот же hash схемы и входы.
- Ошибки trusted setup: перекачайте и проверьте артефакты.
- Верификация on-chain падает: проверьте gas и кодирование входов.

## Валидация
1. Схема компилируется через `circom` без ошибок
2. Генерация доказательства укладывается в приемлемое время
3. Верификация проходит для валидных доказательств и падает для невалидных
4. Публичные входы раскрываются корректно, приватные — остаются скрытыми
