set -ex

for num in {4..10}; do
  python scrape_html.py /tmp/Common\ Scorecard-${num}.html
  cd pdfs
  wget -i ../Common\ Scorecard-${num}.html.links.txt -T 1 --timeout 10
  cd ..
done

