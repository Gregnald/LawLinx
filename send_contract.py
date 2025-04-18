import json
import asyncio
from anchorpy import Program, Provider, Wallet, Context, Idl
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient

# Constants (Double-check these paths!)
#PROGRAM_ID = Pubkey.from_string("CcJa1EaKQBsKTMwx2oFndnz6xXfhwQ1taHEZ9s7eRxip")
PROGRAM_ID = Pubkey.from_string("8AoyHHnTc3os3WL1w8YJPj8yJdsqD4GUt15upS66Pus8")
KEYPAIR_PATH = "/home/kali/.config/solana/id.json"
SYS_PROGRAM_ID = Pubkey.from_string("11111111111111111111111111111111")

async def send_contract(party_a, party_b, clause):
    # Load wallet from keypair
    with open(KEYPAIR_PATH, "r") as f:
        secret = json.load(f)
    kp = Keypair.from_bytes(bytes(secret))
    wallet = Wallet(kp)

    # Connect to Solana Devnet
    client = AsyncClient("https://api.devnet.solana.com")
    provider = Provider(client, wallet)

    # IDL definition exactly matching your Rust contract
    idl_dict = {
        "version": "0.0.1",
        "name": "lawlinx",
        "instructions": [
            {
                "name": "create_contract",
                "accounts": [
                    {"name": "contract", "isMut": True, "isSigner": False},
                    {"name": "creator", "isMut": True, "isSigner": True},
                    {"name": "system_program", "isMut": False, "isSigner": False}
                ],
                "args": [
                    {"name": "party_a", "type": "string"},
                    {"name": "party_b", "type": "string"},
                    {"name": "clause", "type": "string"}
                ]
            }
        ]
    }

    idl = Idl.from_json(json.dumps(idl_dict))
    program = Program(idl, PROGRAM_ID, provider)

    # Derive unique PDA (on-chain address) for the contract
    seeds = [
        b"contract",
        bytes(kp.pubkey()),
        party_a.encode('utf-8'),
        party_b.encode('utf-8')
    ]
    pda, _ = Pubkey.find_program_address(seeds, PROGRAM_ID)

    # Execute the transaction
    try:
        tx = await program.rpc["create_contract"](
            party_a, party_b, clause,
            ctx=Context(
                accounts={
                    "contract": pda,
                    "creator": kp.pubkey(),
                    "system_program": SYS_PROGRAM_ID
                },
            )
        )
        print(f"\n✅ Contract successfully sent to Solana!")
        print(f"🔗 Transaction Signature: {tx}\n")
    except Exception as e:
        print(f"\n❌ Error during contract creation: {e}\n")
    finally:
        await client.close()

# CLI entry point
if __name__ == "__main__":
    print("\n🔐 LawLinx On-Chain Contract Submission 🔐")
    party_a = input("Enter Party A Name: ")
    party_b = input("Enter Party B Name: ")
    clause = input("Enter Contract Clause: ")
    asyncio.run(send_contract(party_a, party_b, clause))
