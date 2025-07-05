import os
import sys
import argparse
from datetime import datetime

def parse_config(config_path):
    configs = []
    current = {}
    with open(config_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    for line in lines:
        upper_line = line.upper()
        if upper_line.startswith('#'):
            if current:
                configs.append(current)
            current = {'root': False, 'search': '', 'ignore': []}
            if ':ROOT' in upper_line:
                current['root'] = True
        elif upper_line.startswith('SEARCH:'):
            current['search'] = line.split(':',1)[1].strip()
        elif upper_line.startswith('IGNORE:'):
            current['ignore'] = [s.strip() for s in line.split(':',1)[1].split(';') if s.strip()]
    if current:
        configs.append(current)
    return configs

def should_ignore_path(path, ignore_patterns, base_path):
    """Check if a path should be ignored based on ignore patterns"""
    for pattern in ignore_patterns:
        # Handle both absolute and relative patterns
        if os.path.isabs(pattern):
            ignore_path = os.path.normpath(pattern)
        else:
            ignore_path = os.path.normpath(os.path.join(base_path, pattern))
        
        # Check if the current path starts with or matches the ignore pattern
        normalized_path = os.path.normpath(path)
        if normalized_path.startswith(ignore_path) or normalized_path == ignore_path:
            return True
    return False

def combine_files(config_file, output_dir="./combined-files"):
    os.makedirs(output_dir, exist_ok=True)
    configs = parse_config(config_file)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join(output_dir, f"combined-{timestamp}.txt")
    
    total_files = 0
    
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for cfg in configs:
            print(f"Processing config: {cfg}")
            
            if cfg['root']:
                base_path = os.getcwd()
                search_path = os.path.normpath(os.path.join(base_path, cfg['search']))
            else:
                search_path = os.path.normpath(cfg['search'])
            
            print(f"Searching in: {search_path}")
            print(f"Ignore patterns: {cfg['ignore']}")
            
            if not os.path.exists(search_path):
                print(f"⚠️  Warning: Search path '{search_path}' does not exist")
                continue

            files_found = 0
            for dirpath, dirnames, filenames in os.walk(search_path):
                # Filter out ignored directories
                original_dirnames = dirnames.copy()
                dirnames[:] = [
                    d for d in dirnames
                    if not should_ignore_path(os.path.join(dirpath, d), cfg['ignore'], search_path)
                ]
                
                if len(dirnames) < len(original_dirnames):
                    ignored_dirs = set(original_dirnames) - set(dirnames)
                    print(f"Ignoring directories: {ignored_dirs}")
                
                # Process files in current directory
                for filename in sorted(filenames):
                    if filename.lower().endswith(('.txt', '.md')):
                        file_path = os.path.join(dirpath, filename)
                        
                        # Check if file should be ignored
                        if should_ignore_path(file_path, cfg['ignore'], search_path):
                            print(f"Ignoring file: {file_path}")
                            continue
                        
                        print(f"Processing file: {file_path}")
                        files_found += 1
                        out_f.write(f"=== {file_path} ===\n")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as in_f:
                                content = in_f.read()
                                out_f.write(content)
                                if not content.endswith('\n'):
                                    out_f.write('\n')
                                out_f.write("\n")
                        except Exception as e:
                            out_f.write(f"[Error reading {file_path}: {e}]\n\n")
            
            print(f"Found {files_found} files in this config")
            total_files += files_found
    
    print(f"✅ Combined file created at: {output_file}")
    print(f"📁 Total files processed: {total_files}")

def main():
    parser = argparse.ArgumentParser(
        description="Combine all .txt and .md files under specified folders into one file."
    )
    parser.add_argument("config", help="Path to your config file")
    parser.add_argument("-o", "--output-dir", default="./combined-files",
                        help="Directory to save the combined file (default: ./combined-files)")
    args = parser.parse_args()

    if not os.path.isfile(args.config):
        print(f"❌ Config file '{args.config}' does not exist.")
        sys.exit(1)

    combine_files(args.config, args.output_dir)

if __name__ == "__main__":
    main()
