import numpy as np
import matplotlib.pyplot as plt
import random

total_questions = 100  
total_time = 200      

def calculate_probabilities(t):
    pc = 0.6 + (2 * t - 40) / 1000
    pw = 0.2 + (30 - t) / 1000
    pb = 1 - (pc + pw)
    return pc, pw, pb

def factorial(n):
    return np.math.factorial(n)

def combination(n, k):
    if 0 <= k <= n:
        return factorial(n) / (factorial(k) * factorial(n - k))
    else:
        return 0 

def binom_pmf(k, n, p):
    coeff = np.math.comb(n, k)
    return coeff * (p ** k) * ((1 - p) ** (n - k))

def calculate_exam_score(correct_answers, incorrect_answers):
    net_correct = correct_answers - incorrect_answers // 4
    score = max(net_correct * 5, 0)  
    return score

def simulate_exam_rest(correct_so_far, incorrect_so_far, blank_so_far, total_time, total_questions):
    correct_answers = correct_so_far
    incorrect_answers = incorrect_so_far

    
    for question_num in range(correct_so_far + incorrect_so_far + blank_so_far + 1, total_questions + 1):
        remaining_time = total_time - ((question_num - 1) * (total_time / total_questions))
        pc, pw, _ = calculate_probabilities(remaining_time)

        
        answer_outcome = np.random.random()
        if answer_outcome < pc:
            correct_answers += 1
        elif answer_outcome < pc + pw:
            incorrect_answers += 1

    score = calculate_exam_score(correct_answers, incorrect_answers)
    return score >= 200  

def probability_of_scoring_above_M_with_blanks(M, pc, pw, total_questions, min_blanks, simulations=10000):
    random.seed(1000)  
    count_above_M = 0

    for _ in range(simulations):
        blank_answers = min_blanks + random.randint(0, total_questions - min_blanks)  
        remaining_questions = total_questions - blank_answers

        correct_answers = 0
        incorrect_answers = 0
        for _ in range(remaining_questions):
            rand_num = random.random()
            if rand_num < pc:
                correct_answers += 1
            elif rand_num < pc + pw:
                incorrect_answers += 1

        score = calculate_exam_score(correct_answers, incorrect_answers)
        if score > M:
            count_above_M += 1

    return count_above_M / simulations

# part a
def plot_pmf_a():
    pc, pw, pb = calculate_probabilities(200)

    x_values = np.arange(0, total_questions + 1)
    px = [binom_pmf(k, total_questions, pc) for k in x_values]
    py = [binom_pmf(k, total_questions, pw) for k in x_values]
    pz = [binom_pmf(k, total_questions, pb) for k in x_values]


    

    plt.figure(figsize=(6, 4))
    plt.bar(x_values, px, color='blue')
    plt.title('PMF of Correct Answers (Px)')
    plt.xlabel('Number of Correct Answers')
    plt.ylabel('Probability')
    plt.savefig('pxpmf.png')
    plt.show()

   
    plt.figure(figsize=(6, 4))
    plt.bar(x_values, py, color='red')
    plt.title('PMF of Incorrect Answers (Py)')
    plt.xlabel('Number of Incorrect Answers')
    plt.ylabel('Probability')
    plt.savefig('pypmf.png')
    plt.show()

    
    plt.figure(figsize=(6, 4))
    plt.bar(x_values, pz, color='green')
    plt.title('PMF of Blank Answers (Pz)')
    plt.xlabel('Number of Blank Answers')
    plt.ylabel('Probability')
    plt.savefig('pzpmf.png')
    plt.show()

# part b
def calculate_b():
    M = int(input("Enter the minimum score (M) between 0 and 500 to calculate the probability: "))
    if M < 0 or M > 500:
        raise ValueError("Score must be between 0 and 500.")
    
    pc, pw, _ = calculate_probabilities(total_time)
    simulations = 10000
    count_above_M = 0
    
    np.random.seed(1000)
    for _ in range(simulations):
        correct_answers = 0
        incorrect_answers = 0

        
        for question_num in range(1, total_questions + 1):
            remaining_time = total_time - (question_num - 1) * (total_time / total_questions)
            pc, pw, _ = calculate_probabilities(remaining_time)

            
            answer_outcome = np.random.random()
            if answer_outcome < pc:
                correct_answers += 1
            elif answer_outcome < pc + pw:
                incorrect_answers += 1

        score = calculate_exam_score(correct_answers, incorrect_answers)
        if score > M:
            count_above_M += 1

    probability_over_M = count_above_M / simulations
    print(f"b-) mtMor{M}: {probability_over_M}")



# part c
def calculate_c():
    remaining_time = 120  
    correct_so_far = 20
    incorrect_so_far = 7
    blank_so_far = 4
    remaining_questions = total_questions - (correct_so_far + incorrect_so_far + blank_so_far)

    np.random.seed(1000)
    simulations = 10000
    pass_count = 0

    for _ in range(simulations):
        if simulate_exam_rest(correct_so_far, incorrect_so_far, blank_so_far, remaining_time, remaining_questions):
            pass_count += 1

    probability_passing = pass_count / simulations
    print(f"c-) s: {probability_passing}")
    return probability_passing




# part d
def calculate_d(original_probability_over_400):
    pc, pw, _ = calculate_probabilities(200)  
    probability_over_400_with_blanks = probability_of_scoring_above_M_with_blanks(400, pc, pw, total_questions, 8)
    if probability_over_400_with_blanks != original_probability_over_400:
        print("d-) news:", probability_over_400_with_blanks)
    else:
        print("d-) news:", original_probability_over_400)


def calculate_phase_probabilities(time_left, questions_in_phase):
    correct_answers = 0
    incorrect_answers = 0

    for question_num in range(1, questions_in_phase + 1):
        
        adjusted_time = time_left - ((question_num - 1) * (time_left / questions_in_phase))
        pc, pw, _ = calculate_probabilities(adjusted_time)

        # Simulate the answer for each question
        answer_outcome = np.random.random()
        if answer_outcome < pc:
            correct_answers += 1
        elif answer_outcome < pc + pw:
            incorrect_answers += 1

    return correct_answers, incorrect_answers
# part e
def calculate_e():
    random.seed(1000)
    simulations = 10000
    count_below_300 = 0

    for _ in range(simulations):
        
        time_left_phase_1 = 200 - 4  
        time_left_phase_2 = time_left_phase_1 - 40 - 6  
        time_left_phase_3 = time_left_phase_2 - 40  
        
        
        correct_1, incorrect_1 = calculate_phase_probabilities(time_left_phase_1, 20)
        correct_2, incorrect_2 = calculate_phase_probabilities(time_left_phase_2, 30)
        correct_3, incorrect_3 = calculate_phase_probabilities(time_left_phase_3, 50)

        total_correct = correct_1 + correct_2 + correct_3
        total_incorrect = incorrect_1 + incorrect_2 + incorrect_3

        score = calculate_exam_score(total_correct, total_incorrect)
        if score < 300:
            count_below_300 += 1

    probability_below_300 = count_below_300 / simulations
    print(f"e-) lt300: {probability_below_300}")
    return probability_below_300


# part g
def calculate_g():
    n = 2  
    lam = 1/40  
    simulations = 10000
    count_between_60_80 = 0

    for _ in range(simulations):
        
        erlang_value = sum(np.random.exponential(scale=1/lam, size=n))

        
        if 60 <= erlang_value <= 80:
            count_between_60_80 += 1

    probability_between_60_80 = count_between_60_80 / simulations
    print(f"g-) b6080: {probability_between_60_80}")
    
    x_values = np.linspace(0, 160, 400)
    y_values = erlang_pdf(n, lam, x_values)
    plt.figure()
    plt.plot(x_values, y_values, label='Erlang PDF')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Probability Density')
    plt.title('Erlang Distribution PDF')
    plt.legend()
    plt.savefig('erlangpdf.png')
    plt.show()
    
def erlang_pdf(n, lam, x):
    return (lam**n) * (x**(n-1)) * np.exp(-lam * x) / np.math.factorial(n-1)




def main():
    plot_pmf_a()
    probability_over_400_b=calculate_b()
    calculate_c()
    calculate_d(probability_over_400_b)
    calculate_e()
    calculate_g()
    
    
if __name__ == "__main__":
    main()
