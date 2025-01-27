use itertools::Itertools;

use crate::parser::Enum;

impl Enum {
    pub fn to_python_def(&self) -> anyhow::Result<String> {
        Ok(format!(
            r"class {}(enum.IntEnum):
{}

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover",
            self.name,
            self.variants
                .iter()
                .map(|(name, value)| format!(r"    {} = {}", name.replace("None", "None_"), value))
                .join("\n")
        ))
    }
}
