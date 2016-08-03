package main

import (
	"errors"
	"fmt"
	"time"
)

func retryTimeout(retries int) (err error) {
	done := make(chan error)

	go func() {
		// Simulate long running function
		time.Sleep(10 * time.Second)
		fmt.Println("Finally")
		done <- errors.New("err")
	}()

	for retry := 1; retry < retries; retry++ {
		select {
		case err = <-done:
			fmt.Println("We're done here")
			return

		case <-time.After(time.Second * time.Duration(1)):
			fmt.Printf("Timeout %d\n", retry)

			if retry == 11 {
				fmt.Println("Forced exit")
				return
			}

		}
	}

	return
}

func main() {
	_ = retryTimeout(20)
}
