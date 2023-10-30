using Statistics

function bleh(x)
    x = parse.(Float64, readlines(open(x))[13:end])
    round.((mean(x), median(x), std(x)), sigdigits=4)
end
println("(Mean, Median, Std)")
println.(bleh.(("./t1", "./t_light_update", "./t_no_blit", "./t_nothing")))