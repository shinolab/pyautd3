use crate::parser::Const;

use super::PythonType;

impl Const {
    pub fn to_python_def(&self) -> anyhow::Result<String> {
        Ok(format!(
            "{}: {} = {}",
            self.name,
            PythonType::try_from(self.ty.clone())?.0,
            self.value
        ))
    }
}
