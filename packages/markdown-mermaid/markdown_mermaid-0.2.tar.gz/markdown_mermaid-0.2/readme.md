# markdown-mermaid

Mermaid extension for [Python-Markdown](https://github.com/Python-Markdown/markdown). Replaces mermaid tagged code blocks with div elements to be rendered by the Mermaid JavaScript library. The JavaScript itself that is required for rendering of the graphs is not inserted. The library can be acquired from a [CDN](https://www.jsdelivr.com/package/npm/mermaid) or [npm](https://www.npmjs.com/package/mermaid) for example.

## Installation

```bash
pip install markdown-mermaid
```

## Example

This would be replaced:<br>
````
```mermaid
a -> b
```
````

With this:
```
<div class="mermaid">
a -> b
</div>
```

