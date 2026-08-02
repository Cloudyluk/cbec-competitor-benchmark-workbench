# HTML Workbench Usage

The HTML workbench is the ordinary-user version of this skill.

## User Flow

1. Open `cbec-competitor-benchmark-workbench.html`.
2. Enter an OpenAI-compatible API Base URL, API Key, and model name.
3. Fill the fixed competitor and company fields.
4. Choose benchmark focus areas.
5. Click `一键生成网页版调查内容`.
6. Review the rendered report.
7. Download Markdown or PDF.

## Security Notes

- API Key is stored only in the user's browser localStorage.
- The pure frontend version sends requests directly from the browser to the configured API Base URL.
- For team or production use, add a local proxy or backend service so API keys are not exposed to browser requests.

## Best Use

Use the HTML workbench for quick competitor benchmarking and management-ready action plans.
Use the Agent skill for deeper research that requires live web verification, evidence ledgers, and source-by-source review.
