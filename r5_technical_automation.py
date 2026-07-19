name: Automated Technical Agent

on:
  # Allows manual execution from the GitHub Actions page.
  workflow_dispatch:
    inputs:
      custom_market_week:
        description: >
          Target market week, for example W29.
          Leave blank to use the current ISO week automatically.
        required: false
        type: string

  # Every Saturday at 07:00 Singapore/Beijing time.
  # GitHub Actions cron uses UTC.
  schedule:
    - cron: "0 23 * * 5"

jobs:
  audit_and_log:
    runs-on: ubuntu-latest

    permissions:
      contents: write

    steps:
      - name: Checkout active repository branch
        uses: actions/checkout@v4
        with:
          ref: ${{ github.ref }}
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install yfinance pandas mplfinance

      - name: Resolve market week
        shell: bash
        run: |
          if [ -n "${{ github.event.inputs.custom_market_week }}" ]; then
            MARKET_WEEK=$(echo \
              "${{ github.event.inputs.custom_market_week }}" \
              | tr '[:lower:]' '[:upper:]')
            echo "Execution mode: manual override"
          else
            WEEK_NUMBER=$(date +%V)
            MARKET_WEEK="W${WEEK_NUMBER}"
            echo "Execution mode: automatic ISO week"
          fi

          if [[ ! "$MARKET_WEEK" =~ ^W([0-9]{1,2})$ ]]; then
            echo "Invalid market week: $MARKET_WEEK"
            echo "Use a value such as W29."
            exit 1
          fi

          WEEK_NUMBER="${MARKET_WEEK#W}"

          if [ "$WEEK_NUMBER" -lt 1 ] || [ "$WEEK_NUMBER" -gt 53 ]; then
            echo "Week number must be between 1 and 53."
            exit 1
          fi

          printf -v NORMALIZED_WEEK "W%02d" "$WEEK_NUMBER"

          echo "MARKET_WEEK=$NORMALIZED_WEEK" >> "$GITHUB_ENV"
          echo "Resolved market week: $NORMALIZED_WEEK"

      - name: Run R5 technical automation
        run: |
          python r5_technical_automation.py \
            --market-week "${{ env.MARKET_WEEK }}"

      - name: Verify generated outputs
        shell: bash
        run: |
          JSON_FILE="technical_agent_${MARKET_WEEK}.json"
          MARKDOWN_FILE="technical_agent_${MARKET_WEEK}.md"
          CHART_DIRECTORY="charts/${MARKET_WEEK}"

          test -s "$JSON_FILE" || {
            echo "Missing or empty JSON file: $JSON_FILE"
            exit 1
          }

          test -s "$MARKDOWN_FILE" || {
            echo "Missing or empty Markdown file: $MARKDOWN_FILE"
            exit 1
          }

          test -d "$CHART_DIRECTORY" || {
            echo "Missing chart directory: $CHART_DIRECTORY"
            exit 1
          }

          CHART_COUNT=$(find "$CHART_DIRECTORY" \
            -maxdepth 1 -type f -name "*.png" | wc -l)

          if [ "$CHART_COUNT" -lt 3 ]; then
            echo "Expected at least 3 chart files."
            echo "Found: $CHART_COUNT"
            exit 1
          fi

          echo "Generated output verification passed."
          echo "JSON: $JSON_FILE"
          echo "Markdown: $MARKDOWN_FILE"
          echo "Chart directory: $CHART_DIRECTORY"
          find "$CHART_DIRECTORY" \
            -maxdepth 1 -type f -name "*.png" -print

      - name: Commit generated outputs
        shell: bash
        run: |
          git config user.name "Team2 Data Automation Bot"
          git config user.email "bot@team2.financial"

          JSON_FILE="technical_agent_${MARKET_WEEK}.json"
          MARKDOWN_FILE="technical_agent_${MARKET_WEEK}.md"
          CHART_DIRECTORY="charts/${MARKET_WEEK}"

          git add -- \
            "$JSON_FILE" \
            "$MARKDOWN_FILE" \
            "$CHART_DIRECTORY"

          echo "Files staged by this run:"
          git diff --cached --name-status

          if git diff --cached --quiet; then
            echo "No output changes detected."
            echo "The generated files are identical to the repository versions."
          else
            git commit -m \
              "chore(data): update R5 technical outputs ${MARKET_WEEK} [skip ci]"

            echo "Pushing outputs to branch: ${{ github.ref_name }}"
            git push origin "HEAD:${{ github.ref_name }}"
          fi
