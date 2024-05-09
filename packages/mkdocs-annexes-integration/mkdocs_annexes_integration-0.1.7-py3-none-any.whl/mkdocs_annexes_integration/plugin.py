"""
File: mkdocs_annexes_integration/plugin.py
Desc: This file contain the plugin used by mkdocs to integrate annexes as markdown file
Author: Thibaud Briard - BRT, <thibaud.brrd@eduge.ch>
Version: 0.1.4 - 2023-05-10
"""
# Imports...
import os, shutil # used to handle path, dicrectory and file creation, deletion and validation.
import logging # used to log warning and errors for MkDocs among other things
from pdf2image import convert_from_path # used to tranform pdf pages into images

from mkdocs.config.base import Config as base_config # used to create an MkDocs config class derived from MkDocs config base
from mkdocs.plugins import BasePlugin as base_plugin # used to create an MkDocs plugin class derived from MkDocs plugin base
from mkdocs.config import config_options as c # used for config schema type safety
from mkdocs.structure.files import File # used to create File in documentation

# The plugin config options
class AnnexesIntegrationConfig(base_config):
    enabled_if_env = c.Type(str, default='')
    placeholders_when_disabled = c.Type(bool, default=False)
    enable = c.Type(bool, default=True)
    temp_dir = c.Type(str, default='temp_annexes')
    annexes = c.ListOfItems(c.Type(dict))

# The plugin itself
class AnnexesIntegration(base_plugin[AnnexesIntegrationConfig]):

    def __init__(self):
        self._logger = logging.getLogger('mkdocs.annexes-integration')
        self._logger.setLevel(logging.INFO)

        self.enabled = False
        self.total_time = 0
    
    def on_config(self, config):
        # Allow user to enable or disable using environment variable
        if 'enabled_if_env' in self.config:
            env_name = self.config['enabled_if_env']
            if env_name:
                self.enabled = os.environ.get(env_name) == '1'
                if not self.enabled:
                    self._logger.warning(
                        'without annexes integration'
                        f'(set environment variable {env_name} to 1 to enable)'
                    )
                    return
            else:
                self.enabled = True
        else:
            self.enabled = True

        # Create temp_dir in directory of mkdocs.yml
        if self.enabled:
            self.config.temp_dir = os.path.join(os.path.dirname(config.docs_dir), self.config.temp_dir)
            if not os.path.exists(self.config.temp_dir):
                os.mkdir(self.config.temp_dir)
        return config

    def on_files(self, files, config):
        try:
            # Generate markdown files for each annex
            for annex in self.config.annexes:
                # Get absolute path to generated markdown
                title, path = list(annex.items())[0]
                # Determine source and destination path from path option
                src, dest = self.get_src_and_dest(path)
                # Get absolute path for PDF directory
                root = os.path.join(self.config.temp_dir, os.path.splitext(dest)[0])
                # Create a root folder containing the annex
                if not os.path.exists(root):
                    os.makedirs(root)
                # Get extension of file
                extension = os.path.splitext(src)[1][1:]
                # Get absolute path to original file
                original = os.path.join(config.docs_dir, src)
                # skip if original file don't exist
                if os.path.exists(original):
                    embedded = f'{os.path.join(self.config.temp_dir, os.path.splitext(dest)[0])}.md'
                    
                    if self.enabled:
                        self._logger.info(f'Integrating annex "{title}"')
                        # Check if file is a PDF
                        if extension in ['pdf']:
                            # For PDF files each page are transformed into images
                            self._logger.info(f'    With each pages as images')
                            # Get absolute path for PDF images directory
                            source = os.path.join(root, 'source')
                            # Save pages as images in the pdf
                            images = convert_from_path(original, size=(None, 800))
                            # Create source folder to save images
                            if not os.path.exists(source):
                                os.mkdir(source)
                            # Create a markdown file that take care of showing PDF annex
                            with open(embedded, 'w') as f:
                                # Write the title to the file
                                f.write(f'# {title}\n\n')

                                for i in range(len(images)):
                                    # Add leading zeros to the page number
                                    filename = f'page_{i + 1:04}.png'
                                    images[i].save(f'{source}/{filename}', 'PNG')
                                    files.append(File(os.path.join(os.path.splitext(dest)[0], f'source/{filename}'), src_dir=self.config.temp_dir, dest_dir=config.site_dir, use_directory_urls=config.use_directory_urls))

                                    # Write the image link to the file
                                    f.write(f'![Page {i+1}](./{os.path.basename(os.path.splitext(dest)[0])}/source/{filename})\n')
                        else:
                            self._logger.warning(f'file {src} extension isn\'t supported --> skipped')
                        # Removing originals files from list of mkdocs files if they were in the docs directory originaly
                        if os.path.isfile(os.path.join(config.docs_dir, dest)):
                            self._logger.info(f'    Remvoing original annex {src} from processed files list')
                            files.remove(files.get_file_from_path(src))
                        # Adding embedded files in list of mkdocs files
                        path = f'{os.path.splitext(dest)[0]}.md'
                        self._logger.info(f'    Adding embedded annex {dest} to processed files list')
                        files.append(File(path, src_dir=self.config.temp_dir, dest_dir=config.site_dir, use_directory_urls=config.use_directory_urls))
                    elif self.config['placeholders_when_disabled']:
                        # Create a markdown file that take care of showing PDF annex
                        with open(embedded, 'w') as f:
                            # Write the title to the file
                            f.write(f'# {title}\n\n')
                            f.write(f'The annex at `{src}` was not integrated because annexes integration plugin was not enable.\n\n')
                            f.write(f'To enable the plugin functionnality please do one of the following action:\n\n')
                            f.write(f' - set environment variable `{self.config["enabled_if_env"]}` to 1 before mkdocs command: `{self.config["enabled_if_env"]}=1 mkdocs {{build|serve}}`\n')
                            f.write(f' - remove `enabled_if_env` option in mkdocs.yml under the `plugins > annexes-integration` section\n\n')
                            f.write(f'To disable the creation of placeholders when plugin is disable, remove or set to false the `placeholders_when_disabled` option in mkdocs.yml under the `plugins > annexes-integration` section\n\n')
                        # Removing originals files from list of mkdocs files if they were in the docs directory originaly
                        if os.path.isfile(os.path.join(config.docs_dir, dest)):
                            self._logger.debug(f'    Remvoing original annex {src} from processed files list')
                            files.remove(files.get_file_from_path(src))
                        # Adding embedded files in list of mkdocs files
                        path = f'{os.path.splitext(dest)[0]}.md'
                        self._logger.debug(f'    Adding embedded annex {dest} to processed files list')
                        files.append(File(path, src_dir=self.config.temp_dir, dest_dir=config.site_dir, use_directory_urls=config.use_directory_urls))
                else:
                    self._logger.warning(f'{src} file doesn\'t exist at {original} --> skipped')

        except Exception as e:
            # Remove temp directory in case of any error before raising error
            self._logger.error(f'error with the annexes-integration plugin : {e}')
            if os.path.exists(self.config.temp_dir):
                shutil.rmtree(self.config.temp_dir)
            raise e
        return files
    
    def on_post_build(self, config):
        if self.enabled:
            # Removing temp_dir directory
            self._logger.info(f'Removin annexes temporary directory {self.config.temp_dir}')
            if os.path.exists(self.config.temp_dir):
                shutil.rmtree(self.config.temp_dir)
            return
    
    def get_src_and_dest(self, path):
        # Get src and dest path from path
        if type(path) is dict:
            src = path['src']
            dest = src
            # Remove every ../ from dest if they exist
            while (dest.startswith('../')):
                dest = dest[3:]
            # Get dest from dict if it as been set
            if 'dest' in path:
                dest = path['dest']
                
        # Get src from path and create dest as same as src
        else:
            src = path
            dest = src
            # Remove every ../ from dest if they exist
            while (dest.startswith('../')):
                dest = dest[3:]
        # add underscore if filename is index to prevent mkdocs from rendring it as an index
        if os.path.splitext(os.path.basename(dest))[0] == 'index':
            dest = os.path.join(os.path.dirname(dest), f'_{os.path.basename(dest)}')
        return src, dest
    
    def get_file_ext(self, src):
        return os.path.splitext(src)[1][1:]
    
    def get_orig_path(self, docs_dir, src):
        return os.path.join(docs_dir, src)
    
    def get_temp_path(self):
        return
    
    def get_dest_path(self):
        return
    
    def get_filename(dest):
        return
