
file_path = "instances/my"

file = open(file_path)

line = readline(file)

tokens = split(line)

num_vertices = parse(Int64, tokens[1])

num_edges = parse(Int64, tokens[2])

num_colors = parse(Int64, tokens[3])

weights = Array{Float64}(undef, num_vertices)

line = readline(file)

tokens = split(line)

for i = 1:num_vertices
    weights[i] = parse(Float64, tokens[i])
end

weights

edges = Array{Int64, 2}(undef, (num_edges, 2))

for i = 1:num_edges
    line = readline(file)
    tokens = split(line)
    edges[i, 1] = parse(Int64, tokens[1]) + 1
    edges[i, 2] = parse(Int64, tokens[2]) + 1
end

edges

using GLPKMathProgInterface
using JuMP
using MathProgBase

m=Model(solver=GLPKSolverMIP())

@variable(m, x[1:num_vertices, 1:num_colors], Bin)

@variable(m, s)

@objective(m, Min, s)

for c=1:num_colors
    for e=1:num_edges
        i = edges[e, 1]
        j = edges[e, 2]
        @constraint(m, x[i, c] + x[j, c] <= 1)
    end
end

@constraint(m, [i=1:num_vertices], sum(x[i, c] for c=1:num_colors) == 1)

@constraint(m, [c=1:num_colors], s >= sum(x[i, c]*weights[i] for i=1:num_vertices))

println("Solving...")

function infocallback(cb)
    println(MathProgBase.cbgetmipsolution(cb))
end
addinfocallback(m, infocallback, when = :MIPSol)

timed_result = @timed solve(m)

println("Arquivo: $(file_path)")
println("Status: $(timed_result[1])")
println("Valor da solução: $(getobjectivevalue(m))")
println("Tempo: $(timed_result[2])")
println("Solução:")
for i=1:num_vertices, c=1:num_colors
    if getvalue(x[i,c])==1
        print("$(c - 1) ")
    end
end
