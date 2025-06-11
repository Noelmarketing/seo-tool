import argparse
from .crawler import crawl
from .report import generate_report, export_csv


def main():
    parser = argparse.ArgumentParser(description='Simple SEO analysis tool')
    parser.add_argument('url', help='Base URL to crawl')
    parser.add_argument('--limit', type=int, default=20, help='Maximum pages to crawl')
    parser.add_argument('--output', default='report.csv', help='CSV report path')
    args = parser.parse_args()

    pages = crawl(args.url, limit=args.limit)
    df = generate_report(pages)
    export_csv(df, args.output)
    print(f'Report written to {args.output}')


if __name__ == '__main__':
    main()
