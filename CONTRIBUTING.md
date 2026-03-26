# Contributing to Lumina

First off, thank you for considering contributing to Lumina! It's people like you who make the internet a smarter place.

### The "No-Key" Rule
Lumina is built on the philosophy of **frictionless learning**. We want users to download the script and run it immediately. Therefore, we have one strict rule for new features:

**Do not ask the user for an API Key or Account Creation.** Everything in Lumina must work "out of the box" without requiring the user to sign up for anything.

### How Can I Contribute?

* **Zero-Auth Knowledge Sources:** Know a great public API that doesn't require a login? (e.g., Public Government data, open-source "Fun Fact" endpoints, or public wikis). If it returns JSON and doesn't require an `API_KEY`, we want it.
* **Creative Data Fetching:** We love clever ways to obtain info without keys, such as:
    * **Public RSS Feeds:** Turning science or history feeds into terminal boxes.
    * **Static JSON:** Fetching data from open-source files hosted on GitHub or Gists.
    * **Lightweight Scraping:** Pulling daily insights from public HTML sites using standard libraries.
* **Code Optimization:** Help us make data fetching faster and the terminal UI more responsive.
* **Theme Ideas:** While we love Dracula, we are open to adding more color schemes like *Nord*, *Solarized*, or *Gruvbox*!

### Our Process

1. **Fork** the repository.
2. **Create a Feature Branch** (`git checkout -b feature/AmazingFeature`).
3. **Test for Friction:** Ensure your feature works immediately without a `.env` file or registration.
4. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
5. **Push** to the branch (`git push origin feature/AmazingFeature`).
6. **Open a Pull Request**.

### Code of Conduct
Please be kind and respectful to fellow contributors. We are all here to learn!
