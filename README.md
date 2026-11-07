# Nookara SDK

Client libraries for the [Nookara](https://nookara.cc) API.

| Folder | Package | Install |
|---|---|---|
| [`python/`](python) | [`nookara`](https://pypi.org/project/nookara/) on PyPI | `pip install nookara` |
| [`node/`](node) | [`nookara`](https://www.npmjs.com/package/nookara) on npm | `npm install nookara` |

Both are generated from the same route catalogue (`python/nookara/catalogue.json`, copied to `node/catalogue/`).
Guides: [Python](https://nookara.cc/guides/python-sdk), [Node](https://nookara.cc/guides/node-sdk). Every route: https://nookara.cc/guides/velora-api

## Tests

```bash
cd python && python -m unittest discover -s tests -p "test_*.py"
cd node && npm test
```

## License

MIT, see [LICENSE](LICENSE).
