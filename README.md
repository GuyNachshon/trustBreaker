# trustBreaker
A simple tool to break trust in a the open source supply chain.

## Installation
1. clone the repo and cd into it
2. run `pip install --editable .`
3. run `trustBreaker` and break some trust!

## Usage
Firstly you'll be asked to answer a few questions about the project you're spoofing and the user you are using.
if you want to you can populate the variable ```REPO, USER, EMAIL & GITHUB_TOKEN``` inside the code.
after that you'll be asked to choose a step to break trust,

there are four steps to breaking trust,
they are displayed in a list with no order.
you can choose any step by pressing the `up` or `down` arrow keys and pressing `enter` to select it.
if there's a multiple choice question you can choose the answer by pressing the `up` or `down` arrow keys and pressing `space` to select it, when done press `enter`.

### Step 1: CELEBRITY CAMEO (aka fake contributors)
This step will add fake contributors to the project.

### Step 2: FAKE COMMIT
This step will add fake commits between 01/01/22 to current date to the project.

### Step 3: SPOOF ACHIEVEMENTS
currently not working - will add fake achievements to the user's profile.
you are more then welcome to try and fix it.

### Step 4: FAKE PROFILE STATS
This step will add fake profile stats to the user's profile.