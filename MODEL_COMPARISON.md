# gpt-oss Model Comparison for MedHelp

The MedHelp application can support both gpt-oss-20b and gpt-oss-120b models. The default to use is the **gpt-oss-20b** for better performance and lower resource requirements.

## Model Comparison

| Feature | gpt-oss-20b | gpt-oss-120b |
|---------|-------------|--------------|
| **Size** | ~22 billion parameters | ~120 billion parameters |
| **Download Size** | ~12-15 GB | ~70 GB |
| **RAM Required** | 4-8 GB | 8-16 GB |
| **Speed** | Faster (5-15 seconds) | Slower (10-30 seconds) |
| **Quality** | Very good medical analysis | Excellent medical analysis |
| **Recommended For** | Most users, development | High-end systems, production |

## How to Switch Models

### Option 1: Environment Variable (Recommended)
```bash
# For gpt-oss-20b (default)
export MODEL_NAME=gpt-oss-20b

# For gpt-oss-120b
export MODEL_NAME=gpt-oss-120b
```

### Option 2: Install and Use gpt-oss-20b
```bash
# Install the 20b model
ollama pull gpt-oss-20b

# Start Ollama
ollama serve

# Run the app (will use 20b by default now)
python main.py
```

### Option 3: Use Both Models
You can have both models installed and switch between them:

```bash
# Install both models
ollama pull gpt-oss-20b
ollama pull gpt-oss-120b

# Check installed models
ollama list

# Switch models by setting environment variable
export MODEL_NAME=gpt-oss-20b    # Use 20b
export MODEL_NAME=gpt-oss-120b   # Use 120b
```

## Performance Recommendations

### For Development/Testing
- **Use gpt-oss-20b**: Faster iteration, good quality results
- Requires less RAM and disk space
- Downloads much faster

### For Production/Best Quality
- **Use gpt-oss-120b**: Better reasoning and more detailed analysis
- Requires more powerful hardware
- Slower but more comprehensive responses

### System Requirements

#### For gpt-oss-20b
- **RAM**: 8 GB minimum, 16 GB recommended
- **Disk**: 20 GB free space
- **CPU**: Any modern processor

#### For gpt-oss-120b
- **RAM**: 16 GB minimum, 32 GB recommended
- **Disk**: 80 GB free space
- **CPU**: High-end processor recommended

## Quality Comparison for Medical Analysis

Both models provide excellent medical guidance, but with these differences:

### gpt-oss-20b
- Provides clear, accurate medical analysis
- Good at identifying emergency situations
- Appropriate for general symptom checking
- Faster response times improve user experience

### gpt-oss-120b
- More detailed and nuanced analysis
- Better at complex symptom interpretation
- More comprehensive treatment suggestions
- Superior reasoning for edge cases

## Updated Setup Instructions

### Quick Start with gpt-oss-20b
1. Install Ollama
2. Download the model: `ollama pull gpt-oss-20b`
3. Start Ollama: `ollama serve`
4. Run the app: `python main.py`
5. Access at: `http://localhost:5000`

### Configuration
The app automatically detects which model you have installed. If you have both models, it will use the one specified in the MODEL_NAME environment variable (defaults to gpt-oss-20b).

## Switching Models Live

You can switch models without restarting the application:

1. Set the environment variable: `export MODEL_NAME=gpt-oss-20b`
2. Restart the Flask app: `Ctrl+C` then `python main.py`
3. The new model will be used for all subsequent analyses

## Conclusion

**For most users, gpt-oss-20b is the better choice** because it:
- Downloads 5x faster
- Uses less RAM and disk space
- Provides faster responses
- Still delivers excellent medical analysis quality
- Perfect for the hackathon demonstration

The 120b model is mainly beneficial if you need the absolute highest quality analysis and have powerful hardware available.