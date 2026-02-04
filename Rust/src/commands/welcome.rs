use serenity::all::{CommandData, CommandDataOption, CommandDataOptionValue};
use serenity::builder::{CreateCommand, CreateCommandOption};
use serenity::model::application::CommandOptionType;

pub async fn run(options: &[CommandDataOption]) -> String {
    let mut user_mention = "someone".to_string();
    let mut message = "Welcome!".to_string();

    for opt in options {
        match opt.name.as_str() {
            "user" => {
                if let CommandDataOptionValue::User(user_id) = &opt.value {
                    user_mention = format!("<@{}>", user_id);
                }
            }
            "message" => {
                if let CommandDataOptionValue::String(s) = &opt.value {
                    message = s.clone();
                }
            }
            _ => {}
        }
    }
    format!("{user_mention} {message}")
}

pub fn register() -> CreateCommand {
    CreateCommand::new("welcome")
        .description("Welcome a user")
        .add_option(
            CreateCommandOption::new(CommandOptionType::User, "user", "The user to welcome")
                .required(true),
        )
        .add_option(
            CreateCommandOption::new(CommandOptionType::String, "message", "The message to send")
                .required(true)
                .add_string_choice(
                    "Friendly Welcome Message :)", 
                    "Fuck af")                
        )
}