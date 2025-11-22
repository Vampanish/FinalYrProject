"""Generate RSA key pairs for Alice, Bob, and Charlie"""

from digital_signature import DigitalSignatureManager

try:
    # Generate Alice's keys
    alice = DigitalSignatureManager('alice_private.pem', 'alice_public.pem')
    alice.generate_keys(save=True)
    print('[OK] Alice keys generated')
    
    # Generate Bob's keys
    bob = DigitalSignatureManager('bob_private.pem', 'bob_public.pem')
    bob.generate_keys(save=True)
    print('[OK] Bob keys generated')
    
    # Generate Charlie's keys
    charlie = DigitalSignatureManager('charlie_private.pem', 'charlie_public.pem')
    charlie.generate_keys(save=True)
    print('[OK] Charlie keys generated')
    
    print('\n✓ All RSA keys ready!')
    print('You can now run: python secure_iot_ui.py')
except Exception as e:
    print(f'Error: {e}')
