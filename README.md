# Build

docker build . -t match-tracker:latest

# Run

docker run network host -d -v ${PWD}/config:/app/config match-tracker:latest

Hook up your present working directory config files to the apps
config files. Format and name:
  - name: $PWD/config/team_sheet[1,2].json
