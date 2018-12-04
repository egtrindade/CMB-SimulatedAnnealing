using GLPKMathProgInterface
using JuMP

FILE_NAME = "instances/cmb01"

file = open(FILE_NAME)

lines = readLines(file)
firstLine = split(lines[1])
    n = parse(Int64, firstLine[1]) #get number os vertex
    e = parse(Int64, firstLine[2]) #get number of edges
    k = parse(Int64, firstLine[3]) #get number of colors

secondLine = split(lines[2])
    for i=1:n
        w[i] = parse(Float64, thirdLine[i]) #vertex weights
    end

E = zeros(n,n)
for lineIndex=3:e #get graph edges(u,v)
    currentLine = split(lines[lineIndex])
    u = parse(Int64, currentLine[1]) + 1
    v = parse(Int64, currentLine[2]) + 1
    E[u,v] = 1
end

m = Model(solver=GLPKSolverMIP(msg_lev=GLPK.MSG_ALL, tm_lim=1, out_frq=1))

@variable(m, x[1:n, 1:k], Bin)
@variable(m, b[1:k]) #biggest weight of the colors

@objective(m, Min, b)

@constraints(m,sum([j in 1:k], x[i,j] for i in 1:n) = 1) #(1)
for j=1:k
    for u=1:n
        for v=1:n
        if E[u, v] == 1
            @constraint(m, x[u, c] + x[v, c] <= 1) #(2)
    end
end
@constraints(m >= sum([j in 1:k], x[i,j] * w[i] for i in 1:n)) #(3)

solve(m)    
