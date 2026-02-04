use serenity::{all::ResolvedOption, builder::CreateCommand};

pub fn run(_options: &[ResolvedOption]) -> String {
    "This is a wonderful command!".to_string()
}

pub fn register() -> CreateCommand {
    CreateCommand::new("wonderful_command").description("An Amazing Command")
}