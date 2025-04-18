import json
import asyncio
from anchorpy import Program, Provider, Wallet, Idl
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient

PROGRAM_ID = Pubkey.from_string("8AoyHHnTc3os3WL1w8YJPj8yJdsqD4GUt15upS66Pus8")
KEYPAIR_PATH = "/home/kali/.config/solana/id.json"

async def fetch_contract(party_a, party_b):
    # Load wallet
    with open(KEYPAIR_PATH, "r") as f:
        secret = json.load(f)
    kp = Keypair.from_bytes(bytes(secret))
    wallet = Wallet(kp)

    # Connect
    client = AsyncClient("https://api.devnet.solana.com")
    provider = Provider(client, wallet)

    # Define IDL for reading account
    idl_dict = {
        "version": "0.0.1",
        "name": "lawlinx",
        "instructions": [],
        "accounts": [
            {
                "name": "ContractData",
                "type": {
                    "kind": "struct",
                    "fields": [
                        {"name": "creator", "type": "publicKey"},
                        {"name": "party_a", "type": "string"},
                        {"name": "party_b", "type": "string"},
                        {"name": "clause", "type": "string"}
                    ]
                }
            }
        ]
    }

    idl = Idl.from_json(json.dumps(idl_dict))
    program = Program(idl, PROGRAM_ID, provider)

    # Recreate PDA
    seeds = [
        b"contract",
        bytes(kp.pubkey()),
        party_a.encode('utf-8'),
        party_b.encode('utf-8')
    ]
    pda, _ = Pubkey.find_program_address(seeds, PROGRAM_ID)

    # Try to fetch the on-chain data
    try:
        contract_account = await program.account["ContractData"].fetch(pda)
        await client.close()
        return contract_account
    except Exception:
        await client.close()
        return None
        

if __name__ == "__main__":
    party_a = input("Enter Party A Name (exact match): ")
    party_b = input("Enter Party B Name (exact match): ")
    asyncio.run(fetch_contract(party_a, party_b))
