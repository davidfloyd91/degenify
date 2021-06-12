## Degenify

Deployed at `0xcc3eB2EF87B6872b802b58A98BcACe061Fe054dF`

Consolidate some defi degeneracy you might like to do repeatedly into a single contract call, `apeIntoSushiAndPickle`:

🦧 deposit eth and wbtc into the sushiswap liquidity pool
🦧 take the resulting slp tokens and deposit them in the correpsonding pickle jar
🦧 take the resulting pslp tokens and deposit those in the corresponding pickle farm

_*except*_

... don't do the last step. There's no point, because you didn't write a function to claim pickle rewards. So just leave them in the jar until you do that. In v2. Soon™️.
