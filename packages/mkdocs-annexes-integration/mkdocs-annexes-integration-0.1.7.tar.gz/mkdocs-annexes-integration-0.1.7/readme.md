# mkdocs-annexes-integration

This is a plugin that transforms annex files into images to be integrated in Markdown pages for MkDocs.

## Setup

### Before installing

Before installing this plugin you need to install `poppler-utils` as it is used by `pdf2image` that is required to use this plugin.

#### Install on Linux :

Note: *It depend on your Linux OS*

``` sh
sudo apt-get install poppler-utils
```

``` sh
sudo yum install poppler-utils
```

#### Install on MacOS :

``` sh
brew install poppler
```

#### Install on Windows :

On Windows, you can download the latest binary release of Poppler from the official website and extract the files to a folder. Then, add the folder to the system's PATH environment variable.

### Installing using pip:

`pip install mkdocs-annexes-integration`

## Config

You need to activate the plugin in `mkdocs.yml`:

```yaml
plugins:
  - annexes-integration:
      annexes: # Required (at least 1)
        - Title of the annex A1: path/A/to/an/annex1.pdf # A path to an annex with it's title
        - Title of the annex A2: path/A/to/an/annex2.pdf # Another path to an annex in same folder as the first
        - Title of the annex B1: path/B/to/an/annex1.pdf # Another path to an annex but in different folder as the first two
        - Title of the annex:
            src: ../src/path/to/an/annex/file1.py
            dest: dest/path/to/an/annex/file1.py
        # others annexes...
      temp_dir: "folder_name" # Optional --> Default : temp_annexes
      enabled_if_env: ENABLE_PDF_EXPORT # Optional
      placeholders_when_disabled: true # Optional --> Default : false
```

As you can see, there are two possible ways to integrate an annex: using a simple path or a source path and a destination path. **Both paths need to be relative to `docs_dir`, though**.

Set at least one annex to use this plugin. If you don't have any annex don't add this plugin to the mkdocs plugins list in config file mkdocs.yml

- `annexes` - A list of all the annexes documents. The path from `docs_dir` to an annex file associated to it's title
- `temp_dir` - The temp directory used to generate markdown file for each annex before rendering to HTML. Only set this option if you already have a temp_annexes folder in the root directory (same as mkdocs.yml), which, you should not normally.
- `enabled_if_env` - Setting this option will enable the build only if there is an environment variable set to 1. Integrations of PDF can slow down build process and it's pretty useful to be fast when doing modification to mkdocs files when doing mkdocs serve.
- `placeholders_when_disabled` - This option will generate an mock file at the place of the integrated file to prevent warning from unreferenced link to the page by other pages. It is intended to be used with `enabled_if_env`.

## Usage

Using the command `mkdocs build` or `mkdocs serve` will trigger the plugin if it as been set correctly in config file.

This plugin is intended to be used with `mkdocs-with-pdf` plugin but can be used as it is.

It is also strongly recommended to use it with `mkdocs-material` plugin. Using this plugin without `mkdocs-material` may result in unecessary page break between annex title and annex images.

## Support

This plugin currently support PDF files :

- **PDF files**: The plugin will convert each page of the PDF into images to be integrated on a page

## License

This project is under MIT license see: `license` file for more detail.

## See Also

- [gitlab repo](http://www.gitlab.org/cfpt-mkdocs-plugins/mkdocs-annexes-integration/)
- [mkdocs website](http://www.mkdocs.org/)
- [mkdocs with-pdf plugin](https://github.com/orzih/mkdocs-with-pdf)
- [mkdocs material plugin](https://github.com/squidfunk/mkdocs-material)