from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import pandas as pd

df_recode = pd.DataFrame(columns=['analysis', 'Current token', 'next token', 'Probability of next token in the current setence',
                        'Top 1 probable next token', 'the probability of top 1 probable next token',
                        'Top 2 probable next token', 'the probability of top 2 probable next token',
                        'Top 3 probable next token', 'the probability of top 3 probable next token',
                        'Top 4 probable next token', 'the probability of top 4 probable next token',
                        'Top 5 probable next token', 'the probability of top 5 probable next token',
                        'Top 6 probable next token', 'the probability of top 6 probable next token',
                        'Top 7 probable next token', 'the probability of top 7 probable next token',
                        'Top 8 probable next token', 'the probability of top 8 probable next token',
                        'Top 9 probable next token', 'the probability of top 9 probable next token',
                        'Top 10 probable next token', 'the probability of top 10 probable next token'])

# Load pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Input text with context and analysis parts
descp = "A stick man is talking with a real woman in the office."
caption = "First, let me fill you in."
context = "The context is" + descp + "The caption is"
analysis = caption
input_text = context + analysis

#################################################################################################################
# Note! The input text does not romove punctuations, you can try to remove punctuations and see the difference. #
# You can only modify input_text to achieve it.                                                                 #
#################################################################################################################

# Process the input
input_ids = tokenizer.encode(input_text, return_tensors='pt')
context_length = len(tokenizer.encode(context))

model.eval()  # Set the model to evaluation mode
with torch.no_grad():
    outputs = model(input_ids, labels=input_ids)
    logits = outputs.logits

    # Process each token in the analysis part
    for i in range(context_length-1, len(input_ids[0]) - 1):
        current_token_id = input_ids[0, i]
        current_token = tokenizer.decode([current_token_id])
        next_token = tokenizer.decode([input_ids[0, i + 1]])
        
        # Calculate probability for the current token
        shift_logits = logits[..., :-1, :].contiguous()
        shift_labels = input_ids[..., 1:].contiguous()
        loss_fct = torch.nn.CrossEntropyLoss(reduction='none')
        loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
        token_losses = loss.view(shift_labels.size())
        token_probabilities = torch.exp(-token_losses)
        token_probability = token_probabilities[0, i].item()

        # Calculate top 10 probable next tokens
        next_token_logits = logits[0, i, :]
        next_token_probs = torch.nn.functional.softmax(next_token_logits, dim=-1)
        top_10_tokens = torch.topk(next_token_probs, 10)
        top_10_token_ids = top_10_tokens.indices.tolist()
        top_10_probs = top_10_tokens.values.tolist()

        # Print results
        print(f"\nCurrent token: '{current_token}' - Probability of the next token '{next_token}': {token_probability:.4f}")
        print("Top 10 probable next tokens and their probabilities:")
        for token_id, prob in zip(top_10_token_ids, top_10_probs):
            token = tokenizer.decode([token_id])
            print(f"  {token}: {prob:.4f}")

        # Save results to pandas dataframe as a row
        df_recode = df_recode._append({'analysis': analysis, 'Current token': current_token, 'next token': next_token, 
                                       'Probability of next token in the current setence': token_probability,
                                       'Top 1 probable next token': tokenizer.decode([top_10_token_ids[0]]), 
                                       'the probability of top 1 probable next token': top_10_probs[0],
                                       'Top 2 probable next token': tokenizer.decode([top_10_token_ids[1]]), 
                                       'the probability of top 2 probable next token': top_10_probs[1],
                                       'Top 3 probable next token': tokenizer.decode([top_10_token_ids[2]]), 
                                       'the probability of top 3 probable next token': top_10_probs[2],
                                       'Top 4 probable next token': tokenizer.decode([top_10_token_ids[3]]), 
                                       'the probability of top 4 probable next token': top_10_probs[3],
                                       'Top 5 probable next token': tokenizer.decode([top_10_token_ids[4]]), 
                                       'the probability of top 5 probable next token': top_10_probs[4],
                                       'Top 6 probable next token': tokenizer.decode([top_10_token_ids[5]]), 
                                       'the probability of top 6 probable next token': top_10_probs[5],
                                       'Top 7 probable next token': tokenizer.decode([top_10_token_ids[6]]), 
                                       'the probability of top 7 probable next token': top_10_probs[6],
                                       'Top 8 probable next token': tokenizer.decode([top_10_token_ids[7]]), 
                                       'the probability of top 8 probable next token': top_10_probs[7],
                                       'Top 9 probable next token': tokenizer.decode([top_10_token_ids[8]]), 
                                       'the probability of top 9 probable next token': top_10_probs[8],
                                       'Top 10 probable next token': tokenizer.decode([top_10_token_ids[9]]), 
                                       'the probability of top 10 probable next token': top_10_probs[9]}, ignore_index=True)

# calculate the sum of probabilities of all tokens in the analysis part
analysis_token_probabilities = 0
for j in range(context_length, i + 1):
    analysis_token_probabilities += token_probabilities[0, j].item()
print(f"Sum of probabilities of all tokens in the analysis part: {analysis_token_probabilities:.4f}")

# add a column for the sum of probabilities of all tokens in the analysis part to the dataframe
df_recode['sum of probability'] = analysis_token_probabilities

# save the dataframe to a csv file
df_recode.to_csv('result/GPT2_pred_add_descp.csv', index=False)
