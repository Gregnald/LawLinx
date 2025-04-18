use anchor_lang::prelude::*;

declare_id!("8AoyHHnTc3os3WL1w8YJPj8yJdsqD4GUt15upS66Pus8");

#[program]
pub mod lawlinx {
    use super::*;

    pub fn create_contract(ctx: Context<CreateContract>, party_a: String, party_b: String, clause: String) -> Result<()> {
        let contract = &mut ctx.accounts.contract;
        contract.party_a = party_a;
        contract.party_b = party_b;
        contract.clause = clause;
        contract.creator = *ctx.accounts.creator.key;
        Ok(())
    }
}

#[derive(Accounts)]
#[instruction(party_a: String, party_b: String, clause: String)]
pub struct CreateContract<'info> {
    #[account(
        init,
        payer = creator,
        space = 8 + 32 + (4 + 64)*2 + (4 + 1024),
        seeds = [b"contract", creator.key().as_ref(), party_a.as_bytes(), party_b.as_bytes()],
        bump
    )]
    pub contract: Account<'info, ContractData>,

    #[account(mut)]
    pub creator: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct ContractData {
    pub creator: Pubkey,
    pub party_a: String,
    pub party_b: String,
    pub clause: String,
}
