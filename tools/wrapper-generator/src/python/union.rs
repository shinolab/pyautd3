use crate::parser::Union;

use super::CtypesType;

impl Union {
    pub fn to_python_def(&self) -> anyhow::Result<String> {
        Ok(format!(
            r"class {}(ctypes.Union):
    _fields_ = [{}]",
            self.name,
            self.fields
                .iter()
                .map(|(name, ty)| anyhow::Ok(format!(
                    "(\"{}\", {})",
                    name,
                    CtypesType::try_from(ty.clone())?.0
                )))
                .collect::<Result<Vec<_>, _>>()?
                .join(", ")
        ))
    }
}
