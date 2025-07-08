# build.py
# Author: Michael Valdron
# Date: Feb. 28, 2021

# Imports
import argparse
import errno
import json
import os
import sys
from typing import Any, Dict, List
from pyhtml import head, meta, title

# General config and metadata for document
CONFIG = 'config.json'

# Argument Validation
def validate_args(args: Dict[str, Any]) -> int:
    if os.path.exists(args['output_dir']) and os.path.isfile(args['output_dir']):
        print(f"Path '{args['output_dir']}' is an existing file, please give a valid path to the output directory.")
        return 1
    elif any(map(lambda cf: not os.path.exists(cf), args['content_mds'])):
        print("One of the content files do not exist, please provide content files that exists.")
        return 2
    elif args['css'] and not os.path.exists(args['css']):
        print(f"CSS file '{args['css']}' provided but does not exist, please provide a CSS file that exists.")
        return 3
    elif args['header'] and not os.path.exists(args['header']):
        print(f"MD header file '{args['header']}' provided but does not exist, please provide a header MD file that exists.")
        return 4
    elif args['footer'] and not os.path.exists(args['footer']):
        print(f"MD footer file '{args['footer']}' provided but does not exist, please provide a footer MD file that exists.")
        return 5
    
    return 0

# Create build directory if does not exist
def process_output_dir(outdir: str) -> int:
    try:
        os.makedirs(outdir, exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(outdir):
            print(f"Output directory processing failed: {str(e)}")
            return e.errno
    return 0

# Create output MD and CSS files for md2pdf module
def output_md(content: str, outdir: str, style: str) -> int:
    try:
        with open(os.path.join(outdir, 'content.out.md'), 'w') as md_f:
            md_f.write(content)
        with open(os.path.join(outdir, "style.out.css"), 'w') as css_f:
            css_f.write(style)
    except IOError as e:
        print(f"Error with writing output files: {str(e)}")
        return e.errno
    
    return 0

# Process header content
def process_header(headerfile: str = None) -> str:
    hcontents = ""
            
    if os.path.exists(CONFIG):
        with open(CONFIG, 'r') as config_f:
            config = json.load(config_f)
            meta_keys = filter(lambda k: k != 'title', config.keys())
            hcontents += str(
                head(
                    title(config['title']),
                    *(meta(name=k, content=config[k]) for k in meta_keys)
                )
            )

    if headerfile:
        with open(headerfile, 'r') as header_f:
            hcontents += f"\n{header_f.read()}"

    return hcontents

# Process style content
def process_style(cssfile: str = None) -> str:
    style_content: List[str] = []
    
    # Append header style
    style_content.append('/* ===Header Style=== */')
    style_content.append('@page { @top-left { content: element(header) }; }')
    style_content.append('#header { display: block; position: running(header); }')
    style_content.append('/* ================== */')

    # Append personal styles if specified
    if cssfile:
        style_content.append(f'/* ==={cssfile} Style=== */')
        with open(cssfile, 'r') as css_f:
            style_content.append(css_f.read())
    
    return '\n'.join(style_content)

# Process document contents
def process_md(contents: List[str], outdir: str, cssfile: str = None, headerfile: str = None, footerfile: str = None) -> int:
    out_content: List[str] = []
    out_style: str = ""
    
    try:
        out_style = process_style(cssfile)
        
        out_content.append(process_header(headerfile))

        if footerfile:
            pass
        
        for content_file in contents:
            with open(content_file, 'r') as f:
                out_content.append(f.read())
    except IOError as e:
        print(f"Error with reading input files: {str(e)}")
        return e.errno
    
    return output_md('\n'.join(out_content), outdir, out_style)

# Main
def main(args: Dict[str, Any]) -> int:
    result = validate_args(args)
    if result != 0:
        return result

    result = process_output_dir(args['output_dir'])
    
    if result == 0:
        result = process_md(args['content_mds'], args['output_dir'], cssfile=args['css'], 
            headerfile=args['header'], footerfile=args['footer'])

    return result

# Parse arguments and call main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build templates for md2pdf.')
    parser.add_argument('output_dir', metavar='outdir', type=str, help='Output Directory for generated md2pdf files.')
    parser.add_argument('content_mds', metavar='contentfiles', type=str, nargs='+', help='Content MD files to append in resultant MD file.')
    parser.add_argument('--css', nargs='?', type=str, help='The CSS file for styling the resultant MD file.')
    parser.add_argument('--header', nargs='?', type=str, help='Header MD content to append to resultant MD file.')
    parser.add_argument('--footer', nargs='?', type=str, help='Footer MD content to append to resultant MD file.')
    sys.exit(main(vars(parser.parse_args())))
