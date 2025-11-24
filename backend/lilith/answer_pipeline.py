def lilith_process_answer(prompt, pipe):
    sequences = pipe(
        prompt,
        do_sample=True,
        max_new_tokens=100,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1,
    )
    gen = sequences[0]['generated_text']
    # answer = gen[len(prompt):].strip()
    return gen

