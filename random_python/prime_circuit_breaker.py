#!/usr/bin/env python3
"""
Prime Number Circuit Breaker Demo
=================================

This demonstrates the Circuit Breaker pattern using prime number computation.
The circuit breaker will "trip" after 3 consecutive non-prime numbers and 
wait for 120 seconds before trying again.

Author: Learning Circuit Breaker Pattern
"""

import time
import random
import math
from datetime import datetime, timedelta


# --- Circuit Breaker Implementation ---
class CircuitBreaker:
    """
    Circuit Breaker pattern implementation.
    
    Trips after a configurable number of consecutive failures,
    then blocks operations for a cooldown period.
    """
    
    def __init__(self, failure_threshold=3, cooldown_seconds=120):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        
        # State tracking
        self._tripped_until = 0          # When circuit will close again
        self._consecutive_failures = 0   # Current failure streak
        self._total_failures = 0         # Total failures since start
        self._total_successes = 0        # Total successes since start
        self._last_failure_time = None   # When last failure occurred
        
    def allow(self):
        """Check if operations are allowed (circuit is closed)"""
        return time.time() > self._tripped_until
    
    def trip(self):
        """Trip the circuit breaker (open it)"""
        self._consecutive_failures += 1
        self._total_failures += 1
        self._last_failure_time = time.time()
        
        # Only trip if we've reached the threshold
        if self._consecutive_failures >= self.failure_threshold:
            self._tripped_until = time.time() + self.cooldown_seconds
            print(f"🔴 CIRCUIT BREAKER TRIPPED! {self._consecutive_failures} consecutive failures.")
            print(f"🕒 Waiting {self.cooldown_seconds} seconds before trying again...")
            print(f"🔓 Circuit will reopen at: {datetime.fromtimestamp(self._tripped_until).strftime('%H:%M:%S')}")
    
    def reset(self):
        """Reset the circuit breaker (close it) after success"""
        was_open = not self.allow()
        self._tripped_until = 0
        self._consecutive_failures = 0  # Reset failure streak
        self._total_successes += 1
        
        if was_open:
            print(f"🟢 CIRCUIT BREAKER RESET! Success after cooldown.")
    
    def record_success(self):
        """Record a successful operation"""
        if self.allow():  # Only count if circuit was closed
            self._consecutive_failures = 0  # Reset streak but don't reset circuit if it's open
            self._total_successes += 1
        else:
            # Success while circuit was open - reset it
            self.reset()
    
    def get_stats(self):
        """Get circuit breaker statistics"""
        is_open = not self.allow()
        return {
            "is_open": is_open,
            "consecutive_failures": self._consecutive_failures,
            "total_failures": self._total_failures,
            "total_successes": self._total_successes,
            "failure_threshold": self.failure_threshold,
            "cooldown_seconds": self.cooldown_seconds,
            "next_retry_time": self._tripped_until if is_open else None,
            "seconds_until_retry": max(0, self._tripped_until - time.time()) if is_open else 0,
            "success_rate": self._total_successes / max(1, self._total_successes + self._total_failures) * 100
        }
    
    def get_status_string(self):
        """Get a human-readable status string"""
        stats = self.get_stats()
        if stats["is_open"]:
            return f"🔴 OPEN (retry in {stats['seconds_until_retry']:.1f}s)"
        else:
            return f"🟢 CLOSED ({stats['consecutive_failures']}/{stats['failure_threshold']} failures)"


# --- Prime Number Utilities ---
def is_prime(n):
    """
    Check if a number is prime.
    
    Uses trial division with optimizations:
    - Handle edge cases (n < 2)
    - Check only odd divisors up to sqrt(n)
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    
    return True


def generate_random_number(min_val=5, max_val=1000000):
    """Generate a random number in the specified range"""
    return random.randint(min_val, max_val)


# --- Prime Hunter with Circuit Breaker ---
class PrimeHunter:
    """
    Prime number hunter that uses a circuit breaker to avoid
    wasting CPU during unlucky streaks of non-prime numbers.
    """
    
    def __init__(self, failure_threshold=3, cooldown_seconds=120, min_num=5, max_num=1000000):
        self.circuit_breaker = CircuitBreaker(failure_threshold, cooldown_seconds)
        self.min_num = min_num
        self.max_num = max_num
        self.primes_found = []
        self.attempts = 0
        
    def hunt_prime(self):
        """
        Attempt to find a prime number.
        Returns True if prime found, False if operation was skipped or failed.
        """
        # Check if circuit breaker allows operation
        if not self.circuit_breaker.allow():
            # Don't increment attempts counter when circuit is open
            stats = self.circuit_breaker.get_stats()
            print(f"⏸️  Circuit breaker OPEN - operation blocked (retry in {stats['seconds_until_retry']:.1f}s)")
            return False
        
        self.attempts += 1
        
        # Generate random number and test for primality
        number = generate_random_number(self.min_num, self.max_num)
        print(f"🎲 Attempt #{self.attempts}: Testing {number:,}...", end=" ")
        
        if is_prime(number):
            # SUCCESS! Found a prime
            self.primes_found.append(number)
            self.circuit_breaker.record_success()
            print(f"✅ PRIME! (Total found: {len(self.primes_found)})")
            return True
        else:
            # FAILURE! Not a prime
            self.circuit_breaker.trip()
            print(f"❌ Not prime")
            return False
    
    def get_summary(self):
        """Get a summary of the prime hunting session"""
        cb_stats = self.circuit_breaker.get_stats()
        return {
            "attempts": self.attempts,
            "primes_found": len(self.primes_found),
            "largest_prime": max(self.primes_found) if self.primes_found else None,
            "prime_hit_rate": len(self.primes_found) / max(1, self.attempts) * 100,
            "circuit_breaker": cb_stats,
            "recent_primes": sorted(self.primes_found[-5:], reverse=True)  # Last 5 primes
        }
    
    def print_summary(self):
        """Print a formatted summary"""
        summary = self.get_summary()
        print("\n" + "="*60)
        print("🎯 PRIME HUNTING SUMMARY")
        print("="*60)
        print(f"Total Attempts: {summary['attempts']}")
        print(f"Primes Found: {summary['primes_found']}")
        print(f"Prime Hit Rate: {summary['prime_hit_rate']:.1f}%")
        if summary['largest_prime']:
            print(f"Largest Prime: {summary['largest_prime']:,}")
        
        print(f"\n🔌 Circuit Breaker Stats:")
        cb = summary['circuit_breaker']
        print(f"  Status: {self.circuit_breaker.get_status_string()}")
        print(f"  Success Rate: {cb['success_rate']:.1f}%")
        print(f"  Total Trips: {cb['total_failures']}")
        
        if summary['recent_primes']:
            print(f"\n🏆 Recent Primes Found:")
            for prime in summary['recent_primes']:
                print(f"  {prime:,}")


# --- Main Application ---
def main():
    """
    Main application that demonstrates the circuit breaker pattern
    with prime number computation.
    """
    print("🚀 Prime Number Circuit Breaker Demo")
    print("=====================================")
    print("Hunting for primes in range 5 to 1,000,000")
    print("Circuit breaker trips after 3 consecutive non-primes")
    print("Cooldown period: 120 seconds")
    print("Checking every 1 second...\n")
    
    # Create prime hunter with circuit breaker
    hunter = PrimeHunter(
        failure_threshold=3,
        cooldown_seconds=120,  # 2 minutes
        min_num=5,
        max_num=1000000
    )
    
    start_time = time.time()
    
    try:
        # Main hunting loop
        while True:
            # Check if circuit breaker is open and wait if needed
            if not hunter.circuit_breaker.allow():
                stats = hunter.circuit_breaker.get_stats()
                wait_time = stats['seconds_until_retry']
                if wait_time > 0:
                    print(f"⏸️  Circuit breaker is OPEN. Waiting {wait_time:.1f} seconds until retry...")
                    time.sleep(wait_time + 0.1)  # Add small buffer to ensure circuit is fully reset
                    print(f"⏰ Wait complete! Resuming operations...")
            
            hunter.hunt_prime()
            
            # Print status every 10 attempts
            if hunter.attempts % 10 == 0:
                print(f"\n📊 Status after {hunter.attempts} attempts:")
                print(f"   Primes found: {len(hunter.primes_found)}")
                print(f"   Circuit breaker: {hunter.circuit_breaker.get_status_string()}")
                print("")
            
            # Sleep for 1 second before next attempt (only when circuit is closed)
            if hunter.circuit_breaker.allow():
                time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping prime hunter...")
        
    finally:
        # Print final summary
        elapsed_time = time.time() - start_time
        print(f"\n⏱️  Total runtime: {elapsed_time:.1f} seconds")
        hunter.print_summary()


# --- Configuration and Testing ---
def test_circuit_breaker():
    """Test the circuit breaker with known non-primes"""
    print("🧪 Testing Circuit Breaker with Known Non-Primes")
    print("="*50)
    
    cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=5)  # Short cooldown for testing
    
    # Test some composite numbers
    test_numbers = [4, 6, 8, 9, 10, 11]  # Last one is prime
    
    for i, num in enumerate(test_numbers, 1):
        if cb.allow():
            print(f"Test {i}: Checking {num}...", end=" ")
            if is_prime(num):
                print("PRIME! ✅")
                cb.record_success()
            else:
                print("Not prime ❌")
                cb.trip()
        else:
            print(f"Test {i}: Circuit breaker OPEN - skipping")
        
        print(f"  Status: {cb.get_status_string()}")
        time.sleep(1)
    
    print("\n🎯 Test complete!")


if __name__ == "__main__":
    # Uncomment the line below to run circuit breaker test instead
    # test_circuit_breaker()
    
    # Run the main prime hunting demo
    main()