# DIALOGS - HTMX Native Browser Dialogs

This example demonstrates native browser dialogs using HTMX's `hx-prompt` and `hx-confirm` attributes.

## 🎯 Features

- **Native Browser Dialogs**: Uses browser's built-in prompt and confirm dialogs
- **hx-prompt**: Shows prompt dialog for user input
- **hx-confirm**: Shows confirmation dialog before action
- **HX-Prompt Header**: Server receives user input via HTTP header
- **Combined Dialogs**: Can use both prompt and confirm together
- **Response History**: Tracks all dialog interactions

## 🚀 HTMX Patterns Demonstrated

- `hx-prompt` - Native browser prompt dialog
- `hx-confirm` - Native browser confirmation dialog
- `hx-post` - Form submission
- `hx-target` - Target elements for response display
- `HX-Prompt` - HTTP header containing user input
- `HX-Request` - HTMX request identification

## 📋 How It Works

### Prompt Dialog (`hx-prompt`)
1. User clicks button with `hx-prompt` attribute
2. Browser shows native prompt dialog
3. User enters text and clicks OK
4. HTMX sends request with `HX-Prompt` header containing user input
5. Server processes input and returns response
6. Response is displayed in target element

### Confirmation Dialog (`hx-confirm`)
1. User clicks button with `hx-confirm` attribute
2. Browser shows native confirmation dialog
3. If user clicks OK, HTMX request is sent
4. If user clicks Cancel, no request is made
5. Server processes request and returns response

### Combined Dialogs
- Can use both `hx-prompt` and `hx-confirm` together
- First shows confirmation dialog
- If confirmed, shows prompt dialog
- If both confirmed, sends request with user input

## 🛠️ Server Implementation

### Flask Route
```python
@app.route('/submit', methods=['POST'])
def submit():
    # Get user input from HX-Prompt header
    user_input = request.headers.get('HX-Prompt', '')

    # Process input and return response
    if user_input:
        return f"User entered <i>{user_input}</i>"
    else:
        return "No input provided"
```

### HTMX Headers
- `HX-Prompt`: Contains user input from prompt dialog
- `HX-Request`: Indicates HTMX request
- `HX-Target`: Target element for response
- `HX-Trigger`: Element that triggered the request

## 🎨 HTML Example

```html
<!-- Prompt Dialog -->
<button class="btn btn-primary"
        hx-post="/submit"
        hx-prompt="Enter a string"
        hx-target="#response">
    Prompt Submission
</button>

<!-- Confirmation Dialog -->
<button class="btn btn-secondary"
        hx-post="/submit"
        hx-confirm="Are you sure you want to submit?"
        hx-target="#response">
    Confirm Submission
</button>

<!-- Combined Dialogs -->
<button class="btn btn-danger"
        hx-post="/delete"
        hx-confirm="Are you sure you want to delete?"
        hx-prompt="Enter confirmation text"
        hx-target="#response">
    Delete with Confirmation
</button>
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
cd DIALOGS
python myapp_test.py
```

### Test Coverage
- ✅ Index page loads correctly
- ✅ Submit endpoint with/without HX-Prompt header
- ✅ Special characters and unicode handling
- ✅ Multiple submissions accumulation
- ✅ Delete and clear endpoints
- ✅ HTMX attributes present in HTML
- ✅ Security headers present
- ✅ CSS and favicon included
- ✅ Debugging instructions present
- ✅ JavaScript debugging code present

## 🚀 Try It Out

1. `cd DIALOGS`
2. `uv sync`
3. `uv run myapp.py`
4. Visit http://localhost:5000
5. Try the different dialog examples!

## 🐛 Debugging

1. **Open Developer Tools** (F12) and go to the **Console** tab
2. **Click a dialog button** and watch the console output
3. **Check Network tab** to see the HTMX request headers
4. **Look for HX-Prompt header** in the request
5. **Expected behavior**: Dialog appears, input is sent to server, response updates

## 📚 Based On

This example is based on the official HTMX example: https://htmx.org/examples/dialogs/

## 🔧 Development Notes

- Uses native browser dialogs (no external libraries)
- Server receives user input via `HX-Prompt` header
- Responses are accumulated in a list for demonstration
- Includes comprehensive debugging and logging
- Follows Development Guiding Light principles
- Minimal CSS and JavaScript (HTMX only)
