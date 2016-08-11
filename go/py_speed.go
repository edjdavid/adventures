package main

// This is the py_speed function written in Go

import (
	"fmt"
	"sync"
	"time"
)

func funcSlow(N int64) float64 {
	var d float64
	var i int64

	d = 0.0
	for i = 0; i < N; i++ {
		d += float64((i%3 - 1) * i)
	}

	return d
}

func seq() {
	var sum float64

	for i := 100000; i < 101000; i++ {
		sum += funcSlow(int64(i))
	}

	fmt.Println(sum)
}

func parallel() {
	var wg sync.WaitGroup
	var sum float64

	sum = 0
	s := make(chan int64)
	defer close(s)

	for w := 0; w < 1000; w++ {
		go func() {
			var v int64
			for v = range s {
				sum += funcSlow(v)
				wg.Done()
			}
		}()
	}

	for i := 100000; i < 101000; i++ {
		wg.Add(1)
		s <- int64(i)
	}

	wg.Wait()
	fmt.Println(sum)
}

func main() {
	start := time.Now()
	seq()
	fmt.Println(time.Since(start).Seconds())

	start = time.Now()
	parallel()
	fmt.Println(time.Since(start).Seconds())
}
