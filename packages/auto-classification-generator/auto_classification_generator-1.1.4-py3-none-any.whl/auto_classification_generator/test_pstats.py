from auto_classification_generator.cli import run_cli
import cProfile
import pstats

with cProfile.Profile() as pr:
    run_cli()
pr.dump_stats('cProfile_report.txt')

with open('cProfile_stats_cum.txt','w') as f:
    p = pstats.Stats('cProfile_report.txt',stream=f)
    p.sort_stats('cumtime').print_stats(100)
with open('cProfile_stats_tot.txt','w') as f:
    p = pstats.Stats('cProfile_report.txt',stream=f)
    p.sort_stats('tottime').print_stats(100)    
