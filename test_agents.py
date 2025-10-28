"""Quick test of the translation agents system"""
from translation_agents import Agent1, Agent2, Agent3, Agent4, VectorDistanceCalculator

print("Testing Agent System...")
print("="*80)

# Initialize agents
print("\n1. Initializing agents...")
agent1 = Agent1()
agent2 = Agent2()
agent3 = Agent3()
agent4 = Agent4(agent1, agent2, agent3)
print("✓ Agents initialized")

# Initialize distance calculator
print("\n2. Initializing distance calculator...")
distance_calculator = VectorDistanceCalculator()
print("✓ Distance calculator ready")

# Run a single test iteration
print("\n3. Running test iteration...")
input_sentence, output_sentence = agent4.process()

# Calculate distance
distance = distance_calculator.calculate_distance(input_sentence, output_sentence)
print(f"\n✓ Vectorial Distance: {distance:.4f}")

print("\n" + "="*80)
print("✓ All systems operational!")
print("You can now run: python translation_agents.py")
