use anchor_lang::prelude::*;

declare_id!("FP5VoXiWcKVXy4MuPbB7YHUm1v3aHdJC4rf9XN6MfVoJ");

#[program]
pub mod blockchain_services {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        msg!("Greetings from: {:?}", ctx.program_id);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize {}
