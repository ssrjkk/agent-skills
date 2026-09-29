---
name: zk-proofs
description: "Zero-knowledge proof development"
category: blockchain
tags: [zk-proofs, circom, snarkjs, cryptography, blockchain]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# Zero-Knowledge Proofs

> Build zero-knowledge proof circuits with Circom and integrate them into dApps.

## Quick Start
```circom
// age-check.circom — Prove age >= 18 without revealing age
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
// Generate proof with snarkjs
import { buildPoseidon } from "circomlibjs";

async function generateProof() {
    // Compile circuit
    // circom age-check.circom --r1cs --wasm --sym
    
    // Generate proving/verification keys
    // snarkjs groth16 setup age-check.r1cs pot12_final.ptau circuit.zkey
    
    // Generate witness
    const { proof, publicSignals } = await snarkjs.groth16.fullProve(
        { age: 25, threshold: 18 },
        "age-check.wasm",
        "circuit_final.zkey"
    );
    
    // Verify proof
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

## Key Concepts
ZK proofs let you prove statements without revealing inputs. Circom defines arithmetic circuits. Groth16 produces small, fast-to-verify proofs. Common uses: private transactions, identity verification, and scalability (zk-rollups).

## When to Use
- Privacy-preserving applications (private voting, identity)
- Blockchain scaling (zk-rollups, validiums)
- Verifiable computation (outsource computation with proof)
- Compliance (prove age, KYC, credit score without exposing data)

## Step-by-Step
1. Author the circuit in Citcom: `circom age-check.circom --r1cs --wasm --sym` compiles to constraints, wasm, and symbols.
2. Generate the powers-of-tau ceremony artifact: `snarkjs powersoftau new bn128 12 pot12_0000.ptau` then `snarkjs powersoftau prepare phase2`.
3. Build proving + verification keys: `snarkjs groth16 setup circuit.r1cs pot12_final.ptau circuit.zkey`.
4. Export the verification key and solidity verifier: `snarkjs zkey export verificationkey` and `snarkjs zkey export solidityverifier`.
5. Compute a witness offline with `snarkjs wtns calculate` then generate the proof with `groth16 prove` (timed for tester's threshold).
6. Verify in the dApp: call the on-chain verifier (or `snarkjs groth16 verify`) with public inputs + proof.

## Examples
```javascript
// Client-side proof generation for private age check
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
# On-chain: deploy Verifier.sol, then verify with the packed call data
snarkjs zkey export solidityverifier circuit_final.zkey Verifier.sol
snarkjs generatecall
# paste the returned inputs into `verifier.verifyProof(...)`
```

## Validation
1. Circuit compiles with `circom` without errors
2. Proof generation completes within acceptable time
3. Verification passes for valid proofs, fails for invalid
4. Public inputs are correctly revealed, private inputs are hidden
