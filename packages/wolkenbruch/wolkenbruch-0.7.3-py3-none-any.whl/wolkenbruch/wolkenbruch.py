#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2019 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.

""" Reminds me if it rains """

import statistics
import sys

import geocoder

from .config import Config
from .emailsender import EMailSender
from .precipitationchecker import PrecipitationChecker


__all__ = ["remind_me_if_it_rains"]

# How many hours to look into the future?
N_HOURS = 14


config = Config()

config.argparser.add(
    "--place",
    help="location of precipitation forecast",
    required=True,
)

config.argparser.add(
    "--average_precipitation_rate_threshold",
    help="send notifications when the average precipitation rate exceeds this value",
    type=float,
    default=0.1,
)

config.argparser.add(
    "--max_precipitation_rate_threshold",
    help="send notifications when the maximum precipitation rate exceeds this value",
    type=float,
    default=0.5,
)

config.argparser.add(
    "--email-subject",
    help="Subject line for the e-mail notification",
    default="Pack your rain gear",
)

config.argparser.add(
    "--email-message",
    help="message body of the e-mail notification",
    default=(
        "The average forecast precipitation rate for today is {a:0.2f}, "
        "maximum {m:0.2f} mm/h."
    ),
)

config.argparser.add(
    "--email-from",
    help="e-mail address to send notification messages from",
)

config.argparser.add(
    "--email-to",
    help="receiver e-mail address for notification messages",
)

config.argparser.add(
    "--smtp-host",
    help="SMTP server to send notifications via (host:port)",
    default="localhost:587",
)

config.argparser.add(
    "--smtp-user",
    help="User as which to log in to the SMTP server",
    default="",
)

config.argparser.add(
    "--smtp-password",
    help="Password used to log in to the SMTP server",
    default="",
)


def remind_me_if_it_rains():
    """Remind me if rain is forecast"""

    try:
        lat, lon = geocoder.osm(config.arguments.place).latlng
    except (TypeError, ValueError) as exception:
        raise RuntimeError(
            f"Could not find location ‘{config.arguments.place}’"
        ) from exception

    hourly_precipitation_rates = PrecipitationChecker(
        lat, lon
    ).hourly_precipitation_rates[:N_HOURS]

    average_precipitation_rate = statistics.fmean(hourly_precipitation_rates)
    max_precipitation_rate = max(hourly_precipitation_rates)

    if config.arguments.verbose:
        print(
            (
                "Average precipitation rate in {place:s} is {a:0.2f} mm/h "
                + "over the next 14 hours, maximum {m:0.2f}. "
            ).format(
                place=config.arguments.place,
                a=average_precipitation_rate,
                m=max_precipitation_rate,
            ),
            file=sys.stderr,
            end="",
        )

    if (
        average_precipitation_rate
        > config.arguments.average_precipitation_rate_threshold
        or max_precipitation_rate > config.arguments.max_precipitation_rate_threshold
    ):
        EMailSender(
            config.arguments.email_from,
            config.arguments.email_to,
            config.arguments.email_subject,
            config.arguments.email_message.format(
                a=average_precipitation_rate,
                m=max_precipitation_rate,
            ),
            config.arguments.smtp_host,
            config.arguments.smtp_user,
            config.arguments.smtp_password,
        ).send_message()

        if config.arguments.verbose:
            print(
                "Sending reminder to {:s} ".format(config.arguments.email_to),
                file=sys.stderr,
            )
    else:
        if config.arguments.verbose:
            print(
                "NOT sending reminder to {:s} ".format(config.arguments.email_to),
                file=sys.stderr,
            )
