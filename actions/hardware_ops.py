import psutil

class HardwareOps:
    @staticmethod
    def get_system_stats():
        cpu = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        return f"CPU Usage: {cpu}% | RAM: {memory.used // (1024*1024)}MB / {memory.total // (1024*1024)}MB ({memory.percent}%)"

    @staticmethod
    def get_top_memory_table(limit=6):
        procs = []
        for p in psutil.process_iter(['name', 'memory_info']):
            try:
                name = p.info['name']
                mem = p.info['memory_info'].rss / (1024 * 1024)
                procs.append((name, mem))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        procs = sorted(procs, key=lambda x: x[1], reverse=True)[:limit]
        table =  "┌──────────────────────────────┬──────────────┐\n"
        table += "│ Process Name                 │ Memory (MB)  │\n"
        table += "├──────────────────────────────┼──────────────┤\n"
        for name, mem in procs:
            display_name = (name[:26] + '..') if len(name) > 28 else name
            table += f"│ {display_name:<28} │ {mem:>10.1f} MB │\n"
        table += "└──────────────────────────────┴──────────────┘"
        return table
