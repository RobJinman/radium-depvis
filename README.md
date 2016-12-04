Radium Dependency Visualiser Script
===================================

A script for producing the dependency graphs that appear throughout the Radium documentation.

Example
-------

        ./depvis "radium_bootstrap*=1.1.2;; \
          /network*=1.14.7;; \
          /;; \
          /event_queue=3.12.9;; \
          /collision=2.4.4;;event_queue=3.12.4 \
          /udp_network=1.3.8;network*=1.14.7;event_queue=3.12.1 \
          /fun_game=1.2.3;radium_bootstrap*=1.1.2;collision=2.4.0,network*=1.14.5"

        radium_bootstrap* 1.1.2 ───────────────────▴1.1.2───────────
        network* 1.14.7         ─────────▴1.14.7───│────────▴1.14.5─
                                         │         │        ║       
        event_queue 3.12.9      ─▴3.12.4─│─▴3.12.1─│────────║───────
        collision 2.4.4         ─╨───────│─║───────│─▴2.4.0─║───────
        udp_network 1.3.8       ─────────┴─╨───────│─║──────║───────
        fun_game 1.2.3          ───────────────────┴─╨──────╨───────

