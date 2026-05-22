from flask import Flask, render_template, request

app = Flask(__name__)

def gauss_seidel(A, b, max_iterations=50, tolerance=1e-5):
    n = len(A)
    x = [0.0] * n 
    steps = []
    
    for iteration in range(max_iterations):
        x_old = x.copy()
        
        for i in range(n):
            sum_val = b[i]
            for j in range(n):
                if i != j:
                    sum_val -= A[i][j] * x[j]
            x[i] = sum_val / A[i][i]
            
        steps.append([round(val, 5) for val in x])
        
        error = max(abs(x[i] - x_old[i]) for i in range(n))
        if error < tolerance:
            break
            
    return steps

@app.route('/', methods=['GET', 'POST'])
def index():
    steps = None
    error = None
    
    if request.method == 'POST':
        try:
            matrix_text = request.form['matrix'].strip()
            lines = matrix_text.split('\n')
            
            A = []
            b = []
            
            for line in lines:
                if not line.strip(): continue
                row = [float(val.strip()) for val in line.split(',')]
                A.append(row[:-1])
                b.append(row[-1])
                
            steps = gauss_seidel(A, b)
            
        except Exception as e:
            error = "Invalid input format. Please ensure you enter numbers separated by commas."
            
    return render_template('index.html', steps=steps, error=error)

if __name__ == '__main__':
    app.run(debug=True)
