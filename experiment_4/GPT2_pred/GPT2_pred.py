from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import csv

# Load pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Input sentence
input_text = "First, let me fill you in."
input_ids = tokenizer.encode(input_text, return_tensors='pt')

model.eval()  # Set the model to evaluation mode
with torch.no_grad():  # Disable gradient calculations
    outputs = model(input_ids, labels=input_ids)
    logits = outputs.logits

    # Calculating probabilities of the current tokens
    shift_logits = logits[..., :-1, :].contiguous()
    shift_labels = input_ids[..., 1:].contiguous()
    loss_fct = torch.nn.CrossEntropyLoss(reduction='none')
    loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
    token_losses = loss.view(shift_labels.size())
    token_probabilities = torch.exp(-token_losses)

    # Calculating top 10 probable next tokens for each token
    for i in range(len(input_ids[0]) - 1):
        next_token_logits = logits[0, i, :]
        next_token_probs = torch.nn.functional.softmax(next_token_logits, dim=-1)
        top_10_tokens = torch.topk(next_token_probs, 10)
        top_10_token_ids = top_10_tokens.indices.tolist()
        top_10_probs = top_10_tokens.values.tolist()

        current_token = tokenizer.decode([input_ids[0, i].item()])
        next_tokens_in_sentence = tokenizer.decode([input_ids[0, i+1].item()])
        print(f"\nCurrent token: '{current_token}' - Probability of next token '{next_tokens_in_sentence}' in the current setence: {token_probabilities[0, i].item():.4f}")
        print("Top 10 probable next tokens and their probabilities:")
        for token_id, prob in zip(top_10_token_ids, top_10_probs):
            token = tokenizer.decode([token_id])
            print(f"  {token}: {prob:.4f}")
    
# calculate the sum of probabilities of the current tokens
sum_probabilities = 0
for i in range(len(input_ids[0]) - 1):
    sum_probabilities += token_probabilities[0, i].item()
print(f"Sum of probabilities of the current tokens: {sum_probabilities:.4f}")

# write to csv file
with open('result/GPT2_pred.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['sentence', 'sum of probability', 'Current token', 'next token', 'Probability of next token in the current setence',
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
    for i in range(len(input_ids[0]) - 1):
        next_token_logits = logits[0, i, :]
        next_token_probs = torch.nn.functional.softmax(next_token_logits, dim=-1)
        top_10_tokens = torch.topk(next_token_probs, 10)
        top_10_token_ids = top_10_tokens.indices.tolist()
        top_10_probs = top_10_tokens.values.tolist()

        current_token = tokenizer.decode([input_ids[0, i].item()])
        next_tokens_in_sentence = tokenizer.decode([input_ids[0, i+1].item()])
        writer.writerow([input_text, sum_probabilities, current_token, next_tokens_in_sentence, token_probabilities[0, i].item(),
                            tokenizer.decode([top_10_token_ids[0]]), top_10_probs[0],
                            tokenizer.decode([top_10_token_ids[1]]), top_10_probs[1],
                            tokenizer.decode([top_10_token_ids[2]]), top_10_probs[2],
                            tokenizer.decode([top_10_token_ids[3]]), top_10_probs[3],
                            tokenizer.decode([top_10_token_ids[4]]), top_10_probs[4],
                            tokenizer.decode([top_10_token_ids[5]]), top_10_probs[5],
                            tokenizer.decode([top_10_token_ids[6]]), top_10_probs[6],
                            tokenizer.decode([top_10_token_ids[7]]), top_10_probs[7],
                            tokenizer.decode([top_10_token_ids[8]]), top_10_probs[8],
                            tokenizer.decode([top_10_token_ids[9]]), top_10_probs[9]])

    