use pyo3::prelude::*;
use std::time::{SystemTime, UNIX_EPOCH};

static WORKER_ID_BITS: u8 = 10;
static TIMES_BITS: u8 = 12;
static MAX_TIMES: u16 = 2u16.pow(12);
static START_TIMESTAMP: u128 = 1704067200000;

fn current_timestamp() -> u128 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_millis()
}

#[pyclass]
struct SnowFlakeID {
    #[pyo3(get, set)]
    worker_id: u16,
    last_timestamp: u128,
    current_timestamp: u128,
    times: u32,
}

#[pymethods]
impl SnowFlakeID {
    #[new]
    fn new(worker_id: u16) -> Self {
        Self {
            worker_id,
            last_timestamp: 0,
            current_timestamp: 0,
            times: 0,
        }
    }

    fn reset(&mut self) {
        self.times = 0;
        self.current_timestamp = current_timestamp();
        self.last_timestamp = 0;
    }

    fn new_id(&mut self) -> u128 {
        self.current_timestamp = current_timestamp();

        // 如果当前时间比最后一次调用的时间要早, 说明系统时间出问题了
        while self.current_timestamp < self.last_timestamp {
            println!("时钟校准 ing...");
            self.reset();
        }

        // 如果当前时间和最后一次调用的时间相同, 意味着处在同一生成时间段
        // 如果存在最后的调用时间, 说明至少调用过 1 次了，所以要先把调用次数 + 1 表示预备开始新的调用
        if self.current_timestamp == self.last_timestamp {
            // 调用次数加 1
            self.times += 1;

            // 如果调用次数达到最大调用次数
            if (self.times & u32::from(MAX_TIMES)) > 0 {
                // if self.times == MAX_TIMES {
                // 更新当前时间戳, 直到当前时间和最后调用的时间不同
                // 如果直接更新而不判断当前时间是不是和最后调用时间相同的话,
                // 可能导致在同一生成时间段内又从 0 开始生成, 导致 ID 重复
                while self.current_timestamp == self.last_timestamp {
                    self.current_timestamp = current_timestamp();
                }
                self.times = 0;
            }
        }

        self.last_timestamp = current_timestamp();

        ((self.current_timestamp - START_TIMESTAMP) << WORKER_ID_BITS << TIMES_BITS)
            | u128::from(self.worker_id << TIMES_BITS)
            | u128::from(self.times)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn nnthon(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<SnowFlakeID>()?;
    Ok(())
}
