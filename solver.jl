using JuMP
using GLPKMathProgInterface
using MathProgBase

FILE_NAME = "instances/cmb01"

file = open(FILE_NAME)

lines = readlines(file)

close(file)

firstLine = split(lines[1])
n = parse(Int64, firstLine[1]) #get number os vertex
e = parse(Int64, firstLine[2]) #get number os edges
k = parse(Int64, firstLine[3]) #get number of colors
w = zeros(n)

secondLine = split(lines[2])
for i=1:n
    w[i] = parse(Float64, secondLine[i]) #vertex weights
end

E = zeros(n,n)
for i=3:(e+2) #get graph edges(u,v)
    currentLine = split(lines[i])
    u = parse(Int64, currentLine[1]) + 1
    v = parse(Int64, currentLine[2]) + 1
    E[u,v] = 1
end

m = Model(solver=GLPKSolverMIP(tm_lim=3600000))

@variable(m, x[1:n, 1:k], Bin)
@variable(m, b) #biggest weight of the colors

@objective(m, Min, b)

@constraint(m, [i=1:n], sum(x[i,j] for j=1:k) == 1) #(1)

for j=1:k
    for u=1:n
        for v=1:n
            if E[u, v] == 1
                @constraint(m, x[u, k] + x[v, k] <= 1) #(2)
            end
        end
    end
end

@constraint(m, [j=1:k], b >= sum(x[i,j] * w[i] for i=1:n)) #(3)

solve(m)    
