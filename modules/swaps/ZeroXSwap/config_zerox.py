NATIVE_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
ZEROX_API_KEY = 'f6274776-dc09-4f98-82c8-468efa3c5080'
ZEROX_PERMIT2_ADDRESS = "0x000000000022d473030f116ddee9f6b43ac78ba3"

zerox_execute_address = '0x8eEa3464105eb401Af47c4dEA81812EBA264bF78'
zerox_abi = [{"inputs":[{"internalType": "uint256", "name": "deadline", "type": "uint256"}], "name": "AllowanceExpired", "type": "error"}, {"inputs":[], "name": "ExcessiveInvalidation", "type": "error"}, {"inputs":[{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "InsufficientAllowance", "type": "error"}, {"inputs":[{"internalType": "uint256", "name": "maxAmount", "type": "uint256"}], "name": "InvalidAmount", "type": "error"}, {"inputs":[], "name": "InvalidContractSignature", "type": "error"}, {"inputs":[], "name": "InvalidNonce", "type": "error"}, {"inputs":[], "name": "InvalidSignature", "type": "error"}, {"inputs":[], "name": "InvalidSignatureLength", "type": "error"}, {"inputs":[], "name": "InvalidSigner", "type": "error"}, {"inputs":[], "name": "LengthMismatch", "type": "error"}, {"inputs":[{"internalType": "uint256", "name": "signatureDeadline", "type": "uint256"}], "name": "SignatureExpired", "type": "error"}, {"anonymous":False, "inputs":[{"indexed":True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed":True, "internalType": "address", "name": "token", "type": "address"}, {"indexed":True, "internalType": "address", "name": "spender", "type": "address"}, {"indexed":False, "internalType": "uint160", "name": "amount", "type": "uint160"}, {"indexed":False, "internalType": "uint48", "name": "expiration", "type": "uint48"}], "name": "Approval", "type": "event"}, {"anonymous":False, "inputs":[{"indexed":True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed":False, "internalType": "address", "name": "token", "type": "address"}, {"indexed":False, "internalType": "address", "name": "spender", "type": "address"}], "name": "Lockdown", "type": "event"}, {"anonymous":False, "inputs":[{"indexed":True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed":True, "internalType": "address", "name": "token", "type": "address"}, {"indexed":True, "internalType": "address", "name": "spender", "type": "address"}, {"indexed":False, "internalType": "uint48", "name": "newNonce", "type": "uint48"}, {"indexed":False, "internalType": "uint48", "name": "oldNonce", "type": "uint48"}], "name": "NonceInvalidation", "type": "event"}, {"anonymous":False, "inputs":[{"indexed":True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed":True, "internalType": "address", "name": "token", "type": "address"}, {"indexed":True, "internalType": "address", "name": "spender", "type": "address"}, {"indexed":False, "internalType": "uint160", "name": "amount", "type": "uint160"}, {"indexed":False, "internalType": "uint48", "name": "expiration", "type": "uint48"}, {"indexed":False, "internalType": "uint48", "name": "nonce", "type": "uint48"}], "name": "Permit", "type": "event"}, {"anonymous":False, "inputs":[{"indexed":True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed":False, "internalType": "uint256", "name": "word", "type": "uint256"}, {"indexed":False, "internalType": "uint256", "name": "mask", "type": "uint256"}], "name": "UnorderedNonceInvalidation", "type": "event"}, {"inputs":[], "name": "DOMAIN_SEPARATOR", "outputs":[{"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs":[{"internalType": "address", "name": "", "type": "address"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "address", "name": "", "type": "address"}], "name": "allowance", "outputs":[{"internalType": "uint160", "name": "amount", "type": "uint160"}, {"internalType": "uint48", "name": "expiration", "type": "uint48"}, {"internalType": "uint48", "name": "nonce", "type": "uint48"}], "stateMutability": "view", "type": "function"}, {"inputs":[{"internalType": "address", "name": "token", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint160", "name": "amount", "type": "uint160"}, {"internalType": "uint48", "name": "expiration", "type": "uint48"}], "name": "approve", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"internalType": "address", "name": "token", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint48", "name": "newNonce", "type": "uint48"}], "name": "invalidateNonces", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"internalType": "uint256", "name": "wordPos", "type": "uint256"}, {"internalType": "uint256", "name": "mask", "type": "uint256"}], "name": "invalidateUnorderedNonces", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"components":[{"internalType": "address", "name": "token", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "internalType": "struct IAllowanceTransfer.TokenSpenderPair[]", "name": "approvals", "type": "tuple[]"}], "name": "lockdown", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256", "name": "", "type": "uint256"}], "name": "nonceBitmap", "outputs":[{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs":[{"internalType": "address", "name": "owner", "type": "address"}, {"components":[{"components":[{"internalType": "address", "name": "token", "type": "address"}, {"internalType": "uint160", "name": "amount", "type": "uint160"}, {"internalType": "uint48", "name": "expiration", "type": "uint48"}, {"internalType": "uint48", "name": "nonce", "type": "uint48"}], "internalType": "struct IAllowanceTransfer.PermitDetails[]", "name": "details", "type": "tuple[]"}, {"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "sigDeadline", "type": "uint256"}], "internalType": "struct IAllowanceTransfer.PermitBatch", "name": "permitBatch", "type": "tuple"}, {"internalType": "bytes", "name": "signature", "type": "bytes"}], "name": "permit", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"internalType": "address", "name": "owner", "type": "address"}, {"components":[{"components":[{"internalType": "address", "name": "token", "type": "address"}, {"internalType": "uint160", "name": "amount", "type": "uint160"}, {"internalType": "uint48", "name": "expiration", "type": "uint48"}, {"internalType": "uint48", "name": "nonce", "type": "uint48"}], "internalType": "struct IAllowanceTransfer.PermitDetails", "name": "details", "type": "tuple"}, {"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "sigDeadline", "type": "uint256"}], "internalType": "struct IAllowanceTransfer.PermitSingle", "name": "permitSingle", "type": "tuple"}, {"internalType": "bytes", "name": "signature", "type": "bytes"}], "name": "permit", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"components":[{"components":[{"internalType": "address", "name": "token", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "internalType": "struct ISignatureTransfer.TokenPermissions", "name": "permitted", "type": "tuple"}, {"internalType": "uint256", "name": "nonce", "type": "uint256"}, {"internalType": "uint256", "name": "deadline", "type": "uint256"}], "internalType": "struct ISignatureTransfer.PermitTransferFrom", "name": "permit", "type": "tuple"}, {"components":[{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "requestedAmount", "type": "uint256"}], "internalType": "struct ISignatureTransfer.SignatureTransferDetails", "name": "transferDetails", "type": "tuple"}, {"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "bytes", "name": "signature", "type": "bytes"}], "name": "permitTransferFrom", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"components":[{"components":[{"internalType": "address", "name": "token", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "internalType": "struct ISignatureTransfer.TokenPermissions[]", "name": "permitted", "type": "tuple[]"}, {"internalType": "uint256", "name": "nonce", "type": "uint256"}, {"internalType": "uint256", "name": "deadline", "type": "uint256"}], "internalType": "struct ISignatureTransfer.PermitBatchTransferFrom", "name": "permit", "type": "tuple"}, {"components":[{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "requestedAmount", "type": "uint256"}], "internalType": "struct ISignatureTransfer.SignatureTransferDetails[]", "name": "transferDetails", "type": "tuple[]"}, {"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "bytes", "name": "signature", "type": "bytes"}], "name": "permitTransferFrom", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"components":[{"components":[{"internalType": "address", "name": "token", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "internalType": "struct ISignatureTransfer.TokenPermissions", "name": "permitted", "type": "tuple"}, {"internalType": "uint256", "name": "nonce", "type": "uint256"}, {"internalType": "uint256", "name": "deadline", "type": "uint256"}], "internalType": "struct ISignatureTransfer.PermitTransferFrom", "name": "permit", "type": "tuple"}, {"components":[{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "requestedAmount", "type": "uint256"}], "internalType": "struct ISignatureTransfer.SignatureTransferDetails", "name": "transferDetails", "type": "tuple"}, {"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "bytes32", "name": "witness", "type": "bytes32"}, {"internalType": "string", "name": "witnessTypeString", "type": "string"}, {"internalType": "bytes", "name": "signature", "type": "bytes"}], "name": "permitWitnessTransferFrom", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"components":[{"components":[{"internalType": "address", "name": "token", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "internalType": "struct ISignatureTransfer.TokenPermissions[]", "name": "permitted", "type": "tuple[]"}, {"internalType": "uint256", "name": "nonce", "type": "uint256"}, {"internalType": "uint256", "name": "deadline", "type": "uint256"}], "internalType": "struct ISignatureTransfer.PermitBatchTransferFrom", "name": "permit", "type": "tuple"}, {"components":[{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "requestedAmount", "type": "uint256"}], "internalType": "struct ISignatureTransfer.SignatureTransferDetails[]", "name": "transferDetails", "type": "tuple[]"}, {"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "bytes32", "name": "witness", "type": "bytes32"}, {"internalType": "string", "name": "witnessTypeString", "type": "string"}, {"internalType": "bytes", "name": "signature", "type": "bytes"}], "name": "permitWitnessTransferFrom", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"components":[{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint160", "name": "amount", "type": "uint160"}, {"internalType": "address", "name": "token", "type": "address"}], "internalType": "struct IAllowanceTransfer.AllowanceTransferDetails[]", "name": "transferDetails", "type": "tuple[]"}], "name": "transferFrom", "outputs":[], "stateMutability": "nonpayable", "type": "function"}, {"inputs":[{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint160", "name": "amount", "type": "uint160"}, {"internalType": "address", "name": "token", "type": "address"}], "name": "transferFrom", "outputs":[], "stateMutability": "nonpayable", "type": "function"}]
zerox_execute_abi = [{"inputs":[{"internalType": "bytes20", "name": "gitCommit", "type": "bytes20"}], "stateMutability": "nonpayable", "type": "constructor"}, {"inputs":[{"internalType": "uint256", "name": "i", "type": "uint256"}, {"internalType": "bytes4", "name": "action", "type": "bytes4"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "ActionInvalid", "type": "error"}, {"inputs":[{"internalType": "uint256", "name": "callbackInt", "type": "uint256"}], "name": "CallbackNotSpent", "type": "error"}, {"inputs":[], "name": "ConfusedDeputy", "type": "error"}, {"inputs":[], "name": "ForwarderNotAllowed", "type": "error"}, {"inputs":[], "name": "InvalidOffset", "type": "error"}, {"inputs":[], "name": "InvalidSignatureLen", "type": "error"}, {"inputs":[], "name": "InvalidTarget", "type": "error"}, {"inputs":[], "name": "NotConverged", "type": "error"}, {"inputs":[], "name": "PayerSpent", "type": "error"}, {"inputs":[{"internalType": "uint256", "name": "callbackInt", "type": "uint256"}], "name": "ReentrantCallback", "type": "error"}, {"inputs":[{"internalType": "address", "name": "oldPayer", "type": "address"}], "name": "ReentrantPayer", "type": "error"}, {"inputs":[{"internalType": "uint256", "name": "deadline", "type": "uint256"}], "name": "SignatureExpired", "type": "error"}, {"inputs":[{"internalType": "contract IERC20", "name": "token", "type": "address"}, {"internalType": "uint256", "name": "expected", "type": "uint256"}, {"internalType": "uint256", "name": "actual", "type": "uint256"}], "name": "TooMuchSlippage", "type": "error"}, {"inputs":[{"internalType": "uint8", "name": "forkId", "type": "uint8"}], "name": "UnknownForkId", "type": "error"}, {"anonymous": False, "inputs":[{"indexed": True, "internalType": "bytes20", "name": "", "type": "bytes20"}], "name": "GitCommit", "type": "event"}, {"stateMutability": "nonpayable", "type": "fallback"}, {"inputs":[{"internalType": "address", "name": "", "type": "address"}], "name": "balanceOf", "outputs":[], "stateMutability": "pure", "type": "function"}, {"inputs":[{"components":[{"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "contract IERC20", "name": "buyToken", "type": "address"}, {"internalType": "uint256", "name": "minAmountOut", "type": "uint256"}], "internalType": "struct SettlerBase.AllowedSlippage", "name": "slippage", "type": "tuple"}, {"internalType": "bytes[]", "name": "actions", "type": "bytes[]"}, {"internalType": "bytes32", "name": "", "type": "bytes32"}], "name": "execute", "outputs":[{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "payable", "type": "function"}, {"stateMutability": "payable", "type": "receive"}]