import sys, os, subprocess

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from builder.generator import SiteGenerator

def main():
    print("=" * 60)
    print("Building 机场推荐云 (jichangtuijian.cloud) Static Site...")
    print("=" * 60)
    
    generator = SiteGenerator(base_dir)
    generator.run_all()
    
    print("\n[SUCCESS] Build finished! Static outputs located in 'public/' directory.")

if __name__ == "__main__":
    main()
