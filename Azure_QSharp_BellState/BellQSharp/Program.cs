using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;
using BellQSharp;

class Program
{
    static async Task<int> Main(string[] args)
    {
        int shots = 4096;
        if (args.Length > 0) int.TryParse(args[0], out shots);

        var counts = new Dictionary<string, int> {
            {"00", 0}, {"01", 0}, {"10", 0}, {"11", 0}
        };

        using (var sim = new QuantumSimulator())
        {
            for (int i = 0; i < shots; i++)
            {
                var res = await PrepareAndMeasureBell.Run(sim);
                var r0 = res.Item1 == Result.Zero ? "0" : "1";
                var r1 = res.Item2 == Result.Zero ? "0" : "1";
                counts[r0 + r1]++;
            }
        }

        Console.WriteLine("=== Simulator (QuantumSimulator) ===");
        int total = 0;
        foreach (var v in counts.Values) total += v;
        foreach (var kv in counts)
        {
            double p = (double)kv.Value / total;
            Console.WriteLine($"{kv.Key}: {kv.Value}  ({p:P2})");
        }

        return 0;
    }
}
