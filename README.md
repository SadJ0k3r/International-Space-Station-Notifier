# ISS Tracker

This project allows you to track the International Space Station (ISS) and receive email notifications when it passes over your location.

## Features

- Real-time tracking of the ISS using its current latitude and longitude.
- Sends an email alert when the ISS is overhead.
- Runs continuously, checking every 60 seconds.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/iss-tracker.git
    cd iss-tracker
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Set up your environment variables:

    - Create a `.env` file based on the provided `.env.example`.
    - Replace the placeholders with your actual email credentials.

4. Run the app:

    ```bash
    npm start
    ```

## Usage

1. Make sure your latitude and longitude are correctly set in the `MY_LAT` and `MY_LONG` variables.
2. Execute the script.
3. Receive email notifications when the ISS is overhead.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
