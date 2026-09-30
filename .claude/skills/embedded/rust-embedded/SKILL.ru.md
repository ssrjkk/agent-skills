---
name: rust-embedded
description: "Rust for embedded systems"
category: embedded
tags: [rust-embedded, embedded, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: rust-embedded
---
# Rust Embedded

> Разрабатывайте прошивки для встраиваемых систем на Rust: безопасность, производительность, современный инструментарий.

## Быстрый старт
```rust
//! Blinky для микроконтроллера STM32
#![no_std]
#![no_main]

use cortex_m_rt::entry;
use panic_halt as _;
use stm32f4xx_hal::{
    pac,
    prelude::*,
    timer::Timer,
};
use embedded_hal::digital::OutputPin;

#[entry]
fn main() -> ! {
    let dp = pac::Peripherals::take().unwrap();
    let cp = cortex_m::Peripherals::take().unwrap();

    let rcc = dp.RCC.constrain();
    let clocks = rcc.cfgr.sysclk(48.MHz()).freeze();

    // Настройка пина LED (PC13 на многих платах STM32)
    let gpioc = dp.GPIOC.split();
    let mut led = gpioc.pc13.into_push_pull_output();

    let mut timer = Timer::syst(cp.SYST, 1.Hz(), &clocks);

    loop {
        led.set_high().unwrap();
        timer.wait(); // задержка 1 секунда
        led.set_low().unwrap();
        timer.wait();
    }
}
```

```toml
# .cargo/config.toml — кросс-компиляция
[target.thumbv7em-none-eabihf]
runner = "gdb-multiarch"
rustflags = ["-C", "link-arg=-Tlink.x", "-C", "linker=arm-none-eabi-gcc"]

[build]
target = "thumbv7em-none-eabihf"
```

```rust
// Embedded HAL — абстракции для переносимости
use embedded_hal::{
    blocking::delay::DelayMs,
    digital::OutputPin,
    spi::SpiDevice,
};

fn control_display<D: DelayMs<u32>, P: OutputPin>(
    delay: &mut D,
    reset: &mut P,
) {
    reset.set_low().unwrap();
    delay.delay_ms(10);
    reset.set_high().unwrap();
    delay.delay_ms(100);
}
```

## Ключевые концепции
`#![no_std]` даёт bare-metal код без стандартной библиотеки. Embedded HAL — переносимые абстракции железа. `cortex-m-rt` берёт на себя vector table и startup. Для прошивки и отладки — probe-rs.

## Когда использовать
- Прошивки для ARM Cortex-M, RISC-V микроконтроллеров
- IoT сенсорные узлы и приводы
- Безопасные встраиваемые системы (safety-critical)
- Замена C/C++ на memory-safe Rust

## Пошаговое руководство
1. Выберите плату/таргет: `rustup target add thumbv7em-none-eabihf` для Cortex-M4F или аналог для RISC-V.
2. Настройте линкер: `.cargo/config.toml` с `rustflags` (link.x) и таргетом по умолчанию.
3. Скаффолд `no_std` крейта: `#![no_std]` + `#![no_main]`, добавьте `cortex-m-rt` для startup и panic handler.
4. Подключите HAL: включите фичи периферии `stm32f4xx_hal` (или `nrf-hal`, `esp-hal`) под чип.
5. Прошивка и отладка: используйте `probe-rs`/`cargo embed` (или `openocd + gdb-multiarch`) с конфигом таргета.
6. Проверка на устройстве: замигайте LED, затем проверьте сенсор/UART; контроль размера через `cargo size`.

## Примеры
```rust
// Чтение кнопки и переключение LED через embedded-hal
#![no_std]
#![no_main]
use cortex_m_rt::entry;
use panic_halt as _;
use stm32f4xx_hal::{pac, prelude::*, gpio::Edge};
use embedded_hal::digital::{InputPin, OutputPin};

#[entry]
fn main() -> ! {
    let dp = pac::Peripherals::take().unwrap();
    let rcc = dp.RCC.constrain();
    let clocks = rcc.cfgr.sysclk(48.MHz()).freeze();
    let gpioa = dp.GPIOA.split(&clocks);
    let gpioc = dp.GPIOC.split();

    let mut led = gpioc.pc13.into_push_pull_output();
    let btn = gpioa.pa0.into_pull_up_input();

    loop {
        if btn.is_low().unwrap() {
            led.set_high().unwrap();
        } else {
            led.set_low().unwrap();
        }
        cortex_m::asm::delay(100_000);
    }
}
```
```bash
# Сборка, прошивка и анализ бинарника
cargo build --release
cargo size --release
cargo embed --release   # прошивка через probe-rs по конфигу таргета
```

## Лучшие практики
- `no_std` крейты для bare-metal таргетов.
- Память и стек ограничены и профилированы.
- Прерывания и DMA для I/O; без busy polling.
- Зафиксируйте toolchain и target для воспроизводимых сборок.
- Тестируйте на железе через CI-runner или QEMU.
- RTOS (RTIC/embassy) для конкурентности.

## Устранение неполадок
- Ошибки линковки: проверьте target triple и layout памяти.
- Переполнение стека: увеличьте стек или профилируйте.
- Флаки прерываний: приоритеты и critical sections.
- Нет вывода: проверьте конфиг UART и baud rate.

## Валидация
1. `cargo build --target thumbv7em-none-eabihf` компилируется без std
2. Прошивка загружается в устройство и работает (LED мигает)
3. Вывод UART/сенсора соответствует ожиданиям
4. Бинарник умещается во flash таргета
