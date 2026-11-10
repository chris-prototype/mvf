import os
MEMORY_DIR = "memory"
MEMORY_FILE = "context.md"

class AgentMemory:
    def __init__(self, memory_dir=MEMORY_DIR, memory_file=MEMORY_FILE):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)
        self.memory_file = os.path.join(self.memory_dir, memory_file)
        
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as f:
                f.write("# Agent Memory Log\n\n")

    def read(self) -> str:
        """Reads the agent's current markdown memory context."""
        if not os.path.exists(self.memory_file):
            return "No memory found."
        with open(self.memory_file, "r") as f:
            return f.read()

    def write(self, entry: str):
        """Appends a new event, thought, or milestone to the memory log."""
        with open(self.memory_file, "a") as f:
            f.write(f"- {entry}\n")


if __name__ == "__main__":
    memory = AgentMemory()
    
    print("--- Reading Existing Memory ---")
    print(memory.read())
    
    memory.write("Hello World: Updated memory script using clean configuration constants.")
    
    print("--- Reading Updated Memory ---")
    print(memory.read())